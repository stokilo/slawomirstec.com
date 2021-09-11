import traceback
from datetime import datetime

from chalicelib.dao.migration.migration_0_1_0 import Migration_0_1_0
from chalicelib.dao.migration.migration_0_1_1 import Migration_0_1_1
from chalicelib.dao.migration.migration_0_1_2 import Migration_0_1_2
from chalicelib.dao.migration.migration_0_1_3 import Migration_0_1_3
from chalicelib.dao.migration.migration_0_1_4 import Migration_0_1_4
from chalicelib.dao.migration.migration_0_1_5 import Migration_0_1_5
from chalicelib.dao.migration.shared import DatabaseMigrationDao, MigrationStatus
from packaging import version
MIGRATIONS = [
    Migration_0_1_0(),
    Migration_0_1_1(),
    Migration_0_1_2(),
    Migration_0_1_3(),
    Migration_0_1_4(),
    Migration_0_1_5()
]

class MigrationExecutor:
    """Run migration files for database.
    """

    @staticmethod
    def run_migrations(release_version: str) -> bool:
        db_version = DatabaseMigrationDao.load()

        if db_version.version is None:
            db_version.version = "0.0.0"

        if version.parse(db_version.version) > version.parse(release_version):
            print(f"Migration not necessary, current version in database: {db_version.version}, "
                  f"next release version: {release_version}")
            return True


        # We run all non executed migrations here i.e. update from 0.1.0 to 0.3.0 will run 0.2.0 and 0.3.0
        print(f"Current version in database: {db_version.version}")
        last_success_migration = ""
        for migration in MIGRATIONS:
            try:
                if version.parse(migration.version) < version.parse(db_version.version):
                    print(f"Already done {migration.version} skipping ...")
                else:
                    print(f"Start migration for {migration.version}")
                    migration.migrate()
                    DatabaseMigrationDao.save_migration_record(migration.version, MigrationStatus.SUCCESS)
                    last_success_migration = migration.version
            except Exception as e:
                traceback.print_exc(e)
                DatabaseMigrationDao.save_migration_record(migration.version, MigrationStatus.FAILURE)
                return False

        db_version.previous_version = " " if db_version.version is None else db_version.version
        db_version.version = last_success_migration
        db_version.migration_date = datetime.utcnow()
        db_version.save()

        return True


