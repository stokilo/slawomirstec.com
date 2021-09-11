from botocore.exceptions import ClientError

from chalicelib.dao.migration.shared import BaseMigration
import boto3
import os


class Migration_0_1_4(BaseMigration):

    def __init__(self):
        super().__init__("0.1.4")

    def migrate(self):
        #
        # We use migration to create secrets and not CDK. CDK is not allowing to set secret value because it would be
        # exposed in generated cloudformation templates. We do it during migration phase and read values from env vars.
        #
        super().log("Create Cloudflare secrets")
        region_name = os.environ["PYAWS_CLI_AWS_REGION"]
        session = boto3.session.Session()

        client = session.client(
            service_name="secretsmanager",
            region_name=region_name
        )
        try:
            client.create_secret(Name='PYAWS_CLI_KV_CACHE_NAMESPACE_ID', SecretString=os.environ["PYAWS_CLI_KV_CACHE_NAMESPACE_ID"])
            client.create_secret(Name='PYAWS_CLI_CF_ACCOUNT_ID', SecretString=os.environ["PYAWS_CLI_CF_ACCOUNT_ID"])
            client.create_secret(Name='PYAWS_CLI_CF_API_TOKEN', SecretString=os.environ["PYAWS_CLI_CF_API_TOKEN"])
            client.create_secret(Name='PYAWS_CLI_CF_ZONE_ID', SecretString=os.environ["PYAWS_CLI_CF_ZONE_ID"])
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceExistsException':
                super().log("Secrets already migrated")


