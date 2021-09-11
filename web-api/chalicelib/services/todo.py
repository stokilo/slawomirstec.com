from chalicelib.dao.todo import TodoDao, TodoItemStatus
from chalicelib.model.contact import Status
from chalicelib.model.shared import OnlyStatus
from chalicelib.model.todo import TodoModel, TodoSubmitResult, TodoGetResult, TodosArray
from chalicelib import logger


class TodoService:

    def __init__(self) -> None:
        self.todo_dao = TodoDao()

    def save_todo(self, todo_model: TodoModel) -> TodoSubmitResult:
        result = TodoSubmitResult(todo_model, Status())
        try:
            if len(todo_model.status) > 255 or len(todo_model.subject) > 255 or \
                    len(todo_model.details) > 255 or len(todo_model.label) > 255 or \
                    len(todo_model.category) > 255:
                raise Exception("One of the fields it too long")
            self.todo_dao.create_todo(todo_model)
            result.status.success = True

        except Exception as e:
            logger.exception(e)
            result.status.generic_error()

        return result

    def get_todos(self, status: str) -> TodoGetResult:
        result = TodoGetResult([], Status())
        try:
            if not len(status):
                items = self.todo_dao.get_todos()
            else:
                items = self.todo_dao.get_todos_with_status(TodoItemStatus(status))

            todos = []
            for item in items:
                todo = TodoModel()
                todo.id = item.id
                todo.date = item.date
                todo.subject = item.subject
                todo.details = item.details
                todo.status = item.status
                todo.category = item.category
                todo.label = item.label
                todos.append(todo)

            result.items = todos
            result.status.success = True

        except Exception as e:
            logger.exception(e)
            result.status.generic_error()

        return result

    def batch_update(self, todos_array: TodosArray) -> OnlyStatus:
        result = OnlyStatus(Status())
        try:
            self.todo_dao.batch_update(todos_array)
            result.status.success = True

        except Exception as e:
            logger.exception(e)
            result.status.generic_error()

        return result


todoService = TodoService()
