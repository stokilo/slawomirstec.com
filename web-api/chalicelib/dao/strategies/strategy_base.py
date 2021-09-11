from typing import List, Any
from typing import TypeVar, Generic
from botocore.session import Session
from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex
from pynamodb.models import Model
from chalicelib import logger

T = TypeVar('T')

""" Base strategies for PyAWS

These are entities creating during initial development of the application. They should be destructured and documented
what access patterns are supported.
"""

class BaseEntityForPyAwsV1(Model):
    """
    Base model for all entities stored in dynamodb table: PyAwsV1
    Each entity that inherits from this model will get data stored in table name with this name.
    Table is created during cdk construct process.

    Note: we use single table model approach where all entities are stored in single table
    Note: table name contains version for future migrations (if any will be required).

    This base class is mostly to resolve configuration of DynamoDB table.
    """
    class Meta:
        table_name = "PyAwsV1"
        region = Session().get_config_variable('region')

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    gsi1pk = UnicodeAttribute()
    gsi1sk = UnicodeAttribute()

    def __init__(self, unique_id: str = "", **kwarg):
        super().__init__(**kwarg)
        self.pk = self.get_pk(unique_id)
        self.sk = self.get_sk(unique_id)
        self.gsi1pk = self.get_pk(unique_id)
        self.gsi1sk = self.get_sk(unique_id)

    def prefix(self) -> str:
        """Prefix for single table model design. Required for PK and SK generation.

        Each entity partition key starts with prefix i.e. MY_ENTITY_PREFIX#
        After # we put unique id of the entity, on example of the user it can be

        USER#12912900192-1212-1221-....

        By default SK follows same approach but this can be changed by overriding get_sk function
        """
        raise Exception("Your entity must define a PK/SK prefix for the model.")

    def get_pk(self, unique_id: str):
        """Partition key with prefix in single table model"""
        return f"{self.prefix()}{unique_id}"

    def get_sk(self, unique_id: str):
        """Sort key with prefix in single table model

        This is default implementation where PK = SK. SK is range key and is local secondary index by default.
        """
        return f"{self.prefix()}{unique_id}"


class BaseSingletonEntityForPyAwsV1(BaseEntityForPyAwsV1):
    """Singleton - only single row with fixed pk and sk that is equal to value returned from prefix()
    """
    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.pk = self.get_pk("")
        self.sk = self.get_sk("")
        self.gsi1pk = self.get_pk("")
        self.gsi1sk = self.get_sk("")


# class LSI1Index(LocalSecondaryIndex):
#     """Local secondary index
#     We use single table design, index is provisioned by CDK.
#     Projection type defaults to all, can be overridden by child classes with set of columns that index should return.
#
#     """
#
#     class Meta(BaseEntityForPyAwsV1.Meta):
#         # once you add LSI, you need set its name here
#         #index_name = ''
#         projection = AllProjection()
#
#     pk = UnicodeAttribute(hash_key=True)
#     sk = UnicodeAttribute(range_key=True)


class GSI1Index(GlobalSecondaryIndex):
    """Global secondary index

    We use single table design, index is provisioned by CDK.
    This is generic index and value of SK/PK depends on the entity type.
    Projection type defaults to all, can be overridden by child classes with set of columns that index should return.
    """

    class Meta(BaseEntityForPyAwsV1.Meta):
        # capacities are only used by PynamoDB when table is provisioned, we create table using CDK so we don't need it
        # however API still requires to define these values
        read_capacity_units = 5
        write_capacity_units = 5
        index_name = 'gsi1'
        # Subclasses must provide own projection,  projection was reused across all models, to fix
        # that I init projection for model specific GSI
        # projection = AllProjection()

    gsi1pk = UnicodeAttribute(hash_key=True)
    gsi1sk = UnicodeAttribute(range_key=True)


class BaseDao(Generic[T]):
    """Base class for specific dao
    """

    @staticmethod
    def update(entity: T, actions: List[Any]) -> bool:
        try:
            entity.update(actions=actions)
        except:
            logger.debug(f"Failed to update entity {entity}")
            return False
        return True

    @staticmethod
    def get(entity: T, pk: str, sk: str) -> T:
        try:
            entity = entity.get(hash_key=pk, range_key=sk)
            entity.pk = pk
            entity.sk = sk
        except Exception as e:
            logger.debug(f"Could not find entity by pk {pk}")
        return entity


