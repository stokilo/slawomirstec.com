from datetime import datetime, timezone
from enum import Enum
from typing import List

import ksuid
from botocore.session import Session
from pynamodb.connection import Connection
from pynamodb.indexes import AllProjection
from pynamodb.transactions import TransactWrite

from chalicelib.dao.dashboard import DashboardDao
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from chalicelib.dao.strategies.strategy_base import GSI1Index, BaseEntityForPyAwsV1, BaseDao
from chalicelib.model.dashboard import DashboardLogItemType
from chalicelib.model.request import REQUEST_SCOPE
from chalicelib.model.todo import TodoModel, TodosArray


class TodoItemStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class TodoItemCategory(Enum):
    JAVA = "JAVA"
    PYTHON = "PYTHON"
    SASS = "SASS"


class TodoItemLabel(Enum):
    EDUCATION = "EDUCATION"
    NEW_FRAMEWORK = "NEW_FRAMEWORK"
    PERSONAL = "PERSONAL"


class GSI1IndexTodo(GSI1Index):
    class Meta(GSI1Index.Meta):
        projection = AllProjection()


class UserTodo(BaseEntityForPyAwsV1):

    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    def __init__(self, pk_unique_id: str = "", sk_unique_id = "", **kwarg):
        super().__init__(pk_unique_id, **kwarg)
        self.sk = super().get_sk(sk_unique_id)

    id = UnicodeAttribute()
    date = UTCDateTimeAttribute()
    subject = UnicodeAttribute()
    details = UnicodeAttribute()
    status = UnicodeAttribute()
    category = UnicodeAttribute()
    label = UnicodeAttribute()
    gsi1_index = GSI1IndexTodo()

    def prefix(self) -> str:
        return "USER_TODO#"


class TodoDao(BaseDao[UserTodo]):

    def create_todo(self, todo_model: TodoModel):
        client_id = REQUEST_SCOPE.get().auth_client_id
        item_id = ksuid.ksuid().__str__()

        user_todo = UserTodo(client_id, item_id)
        user_todo.id = item_id
        # sk by ksuid to have latest one sorted
        user_todo.sk = user_todo.get_sk(user_todo.id)
        # access pattern: get by status
        user_todo.gsi1pk = user_todo.get_pk(client_id)
        user_todo.gsi1sk = todo_model.status

        user_todo.date = datetime.now(timezone.utc)
        user_todo.subject = todo_model.subject
        user_todo.details = todo_model.details
        user_todo.status = todo_model.status
        user_todo.category = todo_model.category
        user_todo.label = todo_model.label
        dashboard_dao = DashboardDao()

        # Create user and all accompanied tables
        connection = Connection(region=Session().get_config_variable('region'))
        with TransactWrite(connection=connection) as transaction:
            transaction.save(user_todo)
            dashboard_dao.add_audit_event(transaction, DashboardLogItemType.TODO_CREATION)
            dashboard_dao.update_dashboard(transaction, update_todo=True)

        todo_model.id = user_todo.id

    def get_todos(self) -> List[UserTodo]:
        items = []
        user_todo = UserTodo()
        client_id = REQUEST_SCOPE.get().auth_client_id
        item_iterator = UserTodo.query(user_todo.get_pk(client_id),
                                       limit=20)
        for item in item_iterator:
            items.append(item)
        return items

    def get_todos_with_status(self, status: TodoItemStatus) -> List[UserTodo]:
        items = []
        user_todo = UserTodo()
        client_id = REQUEST_SCOPE.get().auth_client_id
        item_iterator = UserTodo.gsi1_index.query(user_todo.get_pk(client_id),
                                                  UserTodo.gsi1sk == status.name,
                                                  limit=20)
        for item in item_iterator:
            items.append(item)
        return items

    def batch_update(self, todos_array: TodosArray):
        if not len(todos_array.todos):
            return
        connection = Connection(region=Session().get_config_variable('region'))
        user_todo = UserTodo()
        client_id = REQUEST_SCOPE.get().auth_client_id
        with TransactWrite(connection=connection) as transaction:
            for item in todos_array.todos:
                transaction.update(
                    UserTodo(pk_unique_id=client_id, sk_unique_id=item.id),
                    actions=[UserTodo.status.set(item.status), UserTodo.gsi1sk.set(item.status)]
                )

