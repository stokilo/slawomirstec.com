import json
import os
from chalicelib.dao.migration.executor import MigrationExecutor

#
# Ensure not direct execution of this migration
#
allow_to_execute_env = os.environ.get("PYAWS_CLI_ENV_ALLOW_EXECUTE_SHELL_SCRIPT")
if allow_to_execute_env is None or not len(allow_to_execute_env):
    raise Exception("It is not allowed to run this script directly, you can call it only from pyaws-cli.py")

#
# We migrate to version configured for project in release-version.json
#
f = os.path.dirname(__file__) + '/../release-version.json'
with open(f, 'r') as release_version_file:
    release_version = json.loads(release_version_file.read())["version"]

print(f"======================================================================")
print(f"=====Performing database migration to version: {release_version} ===========")
print(f"======================================================================")

migration_ok = MigrationExecutor().run_migrations(release_version)
if not migration_ok:
    raise Exception(f"Migration to version {release_version} failed!!!")

print(f"======================================================================")
print(f"===== Finished database migration to version: {release_version} ============")
print(f"======================================================================")