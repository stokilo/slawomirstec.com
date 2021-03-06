from typing import List

from botocore.session import Session
from pynamodb.connection import Connection
from pynamodb.indexes import AllProjection
from pynamodb.transactions import TransactWrite

from chalicelib.dao.dashboard import DashboardDao
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, MapAttribute
import uuid
from datetime import datetime, timezone

from chalicelib.dao.strategies.strategy_base import GSI1Index, BaseEntityForPyAwsV1, BaseDao
from chalicelib.model.dashboard import DashboardLogItemType


class GSI1IndexUser(GSI1Index):
    class Meta(GSI1Index.Meta):
        projection = AllProjection()


class UserProfile(MapAttribute):
    """User profile complex attribute
    """
    firstName = UnicodeAttribute(null=True, default="")
    lastName = UnicodeAttribute(null=True, default="")
    profileImagePath = UnicodeAttribute(null=True, default="default_assets/default_profile_image.png")


class UserEntity(BaseEntityForPyAwsV1):
    """User entity
    """

    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    def __init__(self, unique_id: str = "", **kwarg):
        super().__init__(unique_id, **kwarg)

    email = UnicodeAttribute(null=False)
    user_id = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)
    secret = UnicodeAttribute(null=False)
    secret_refresh_token = UnicodeAttribute(null=False)
    creation_date = UTCDateTimeAttribute(null=False)
    user_profile = UserProfile(null=True)
    gsi1_index = GSI1IndexUser()

    def prefix(self) -> str:
        return "USER#"


class AuthDao(BaseDao[UserEntity]):

    @staticmethod
    def create_user(email: str, password_hashed: str, secret: str, secret_refresh_token: str) -> UserEntity:
        email = email.lower()
        # autogenerated unique user id, this is used for referencing all entities with the user, email is only for auth
        # we combine hash of 3 characters with uuid in case there is any problem with lambda random generator
        user_id = '-'.join([str(uuid.uuid4()), str(hash(email[0:3]))])

        user = UserEntity(user_id)
        user.user_id = user_id
        user.email = email
        user.password = password_hashed
        user.secret = secret
        user.secret_refresh_token = secret_refresh_token
        user.creation_date = datetime.now(timezone.utc)
        user.user_profile = UserProfile()
        # access pattern: get user by email
        user.gsi1pk = user.get_pk(unique_id=email)
        user.gsi1sk = email
        dashboard_dao = DashboardDao()

        # Create user and all accompanied tables
        connection = Connection(region=Session().get_config_variable('region'))
        with TransactWrite(connection=connection) as transaction:
            transaction.save(user)
            dashboard_dao.add_audit_event(transaction, DashboardLogItemType.USER_CREATION)
            dashboard_dao.update_dashboard(transaction, update_user=True)
        return user


    @staticmethod
    def get_user_by_id(user_id: str) -> UserEntity:
        user_entity = UserEntity()
        return BaseDao.get(user_entity, user_entity.get_pk(user_id), user_entity.get_sk(user_id))

    @staticmethod
    def has_user_with_email(email: str) -> bool:
        email = email.lower()
        return len(AuthDao.get_users_by_email(email)) > 0

    @staticmethod
    def get_users_by_email(email: str) -> List[UserEntity]:
        email = email.lower()
        users = []
        user_entity = UserEntity()
        item_iterator = UserEntity.gsi1_index.query(user_entity.get_pk(unique_id=email),
                                                    UserEntity.gsi1sk == email,
                                                    limit=1)
        for item in item_iterator:
            if item.user_profile is None:
                item.user_profile = UserProfile()
            users.append(item)
        return users
