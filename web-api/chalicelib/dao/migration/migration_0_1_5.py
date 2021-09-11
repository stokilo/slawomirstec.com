from botocore.exceptions import ClientError

from chalicelib.dao.migration.shared import BaseMigration
import boto3
import os


class Migration_0_1_5(BaseMigration):

    def __init__(self):
        super().__init__("0.1.5")

    def migrate(self):
        pass
