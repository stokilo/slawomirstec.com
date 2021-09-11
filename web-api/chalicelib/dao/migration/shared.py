import ksuid
from datetime import datetime
from pycparser.c_ast import Enum
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from packaging import version

from chalicelib.dao.strategies.strategy_base import BaseSingletonEntityForPyAwsV1, BaseEntityForPyAwsV1, BaseDao


class BaseMigration(object):
    """Base class for all migrations scripts
    """

    def __init__(self, version):
        self.version = version

    def migrate(self):
        pass

    def log(self, msg: str):
        print(f"Migration: {self.version} :: {msg}")

    def __hash__(self):
        return hash(self.version)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return version.parse(self.version) == version.parse(other.version)

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return version.parse(self.version) < version.parse(other.version)

    def __gt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return version.parse(self.version) > version.parse(other.version)




class MigrationStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class DbVersionInformation(BaseSingletonEntityForPyAwsV1):
    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    version = UnicodeAttribute(null=False)
    previous_version = UnicodeAttribute(null=False)
    migration_date = UTCDateTimeAttribute()

    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def prefix(self) -> str:
        return "DATABASE_VERSION#INFORMATION#"


class DbMigrationRecord(BaseEntityForPyAwsV1):
    """Entity for migration record, each attempts to migration is saved in audit log for migrations
    """
    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    def __init__(self, unique_id: str = "", **kwarg):
        super().__init__(unique_id, **kwarg)

    version = UnicodeAttribute()
    migration_date = UTCDateTimeAttribute()
    migration_status = UnicodeAttribute()

    def prefix(self) -> str:
        return "DATABASE_VERSION#RECORD#"


class DatabaseMigrationDao(BaseDao[DbVersionInformation]):

    @staticmethod
    def load() -> DbVersionInformation:
        db_version: DbVersionInformation = DbVersionInformation()
        return BaseDao.get(db_version, db_version.get_pk(""), db_version.get_sk(""))

    @staticmethod
    def save_migration_record(version: str, status: MigrationStatus):
        db_migration_record = DbMigrationRecord(ksuid.ksuid().__str__())
        db_migration_record.version = version
        db_migration_record.migration_date = datetime.utcnow()
        db_migration_record.migration_status = status.__str__()
        db_migration_record.save()