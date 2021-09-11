import os

from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    core as cdk
)
from aws_cdk.aws_dynamodb import StreamViewType
from aws_cdk.aws_iam import PolicyStatement, Effect, AnyPrincipal
from aws_cdk.aws_s3 import Bucket, BucketAccessControl, CorsRule, HttpMethods
from aws_cdk.aws_s3_deployment import BucketDeployment, Source
from aws_cdk.core import RemovalPolicy
from cdk_chalice import Chalice


class WebApi(cdk.Stack):

    _API_HANDLER_LAMBDA_MEMORY_SIZE_1024 = 1024
    _API_HANDLER_LAMBDA_MEMORY_SIZE_128 = 128
    _API_HANDLER_LAMBDA_MEMORY_SIZE_256 = 256
    _API_HANDLER_LAMBDA_MEMORY_SIZE_512 = 512

    _API_HANDLER_LAMBDA_TIMEOUT_SHORT_SECONDS = 5
    _API_HANDLER_LAMBDA_TIMEOUT_SECONDS = 10

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #
        # DynamoDb
        #
        partition_key = dynamodb.Attribute(name='pk', type=dynamodb.AttributeType.STRING)
        sort_key = dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING)
        gsi1pk = dynamodb.Attribute(name="gsi1pk", type=dynamodb.AttributeType.STRING)
        gsi1sk = dynamodb.Attribute(name="gsi1sk", type=dynamodb.AttributeType.STRING)

        self.dynamodb_table = dynamodb.Table(
            self, 'WebApiTable',
            partition_key=partition_key,
            sort_key=sort_key,
            table_name="PyAwsV1",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            stream=StreamViewType.NEW_AND_OLD_IMAGES)
        cdk.CfnOutput(self, 'DynamoDbTableName', value=self.dynamodb_table.table_name)
        self.dynamodb_table.add_global_secondary_index(index_name="gsi1", partition_key=gsi1pk, sort_key=gsi1sk)

        #
        # Role for lambda execution with access to dynamodb
        #
        lambda_service_principal = iam.ServicePrincipal('lambda.amazonaws.com')
        cloudwatch_logs_policy = iam.ManagedPolicy.from_aws_managed_policy_name(
            'service-role/AWSLambdaBasicExecutionRole')
        s3_full_access_policy = iam.ManagedPolicy.from_aws_managed_policy_name(
            'AmazonS3FullAccess')

        self.api_handler_iam_role = iam.Role(
            self, 'ApiHandlerLambdaRole', assumed_by=lambda_service_principal,
            managed_policies=[cloudwatch_logs_policy, s3_full_access_policy])
        self.dynamodb_table.grant_read_write_data(self.api_handler_iam_role)
        self.dynamodb_table.grant(self.api_handler_iam_role, 'dynamodb:DescribeTable')
        self.api_handler_iam_role.add_to_policy(PolicyStatement(
            resources=["*"],
            actions=["ssm:GetParameter", "secretsmanager:GetSecretValue"]
        ))

        #
        # Role for lambda that performs periodic task execution
        #
        self.periodic_task_iam_role = iam.Role(
            self, 'PeriodicTaskLambdaRole', assumed_by=lambda_service_principal,
            managed_policies=[cloudwatch_logs_policy])
        self.periodic_task_iam_role.add_to_policy(PolicyStatement(
            resources=["*"],
            actions=["cloudwatch:GetMetricStatistics", "SNS:Publish", "ssm:GetParameter"]
        ))
        self.dynamodb_table.grant_read_write_data(self.periodic_task_iam_role)
        self.dynamodb_table.grant(self.periodic_task_iam_role, 'dynamodb:DescribeTable')

        #
        # Role for lambda used for dynamodb stream processing
        #
        self.on_table_update_iam_role = iam.Role(
            self, 'OnTableUpdateLambdaRole', assumed_by=lambda_service_principal,
            managed_policies=[cloudwatch_logs_policy])
        self.on_table_update_iam_role.add_to_policy(PolicyStatement(
            resources=["*"],
            actions=["ses:SendEmail", "logs:CreateLogGroup", "logs:CreateLogStream",  "logs:PutLogEvents",
                     "dynamodb:ListStreams", "dynamodb:GetShardIterator", "dynamodb:GetRecords",
                     "dynamodb:DescribeStream", "dynamodb:DescribeTable",
                     "dynamodb:BatchGetItem",
                     "dynamodb:Query",
                     "dynamodb:GetItem",
                     "dynamodb:Scan",
                     "dynamodb:BatchWriteItem",
                     "dynamodb:PutItem",
                     "dynamodb:UpdateItem",
                     "dynamodb:DeleteItem",
                     "ssm:GetParameter"]
        ))

        #
        # Chalice config, check details for more details lambda config inside create_chalice_stage_config
        #
        web_api_source_dir = os.path.join(os.path.dirname(__file__), os.pardir,
                                          os.pardir, 'web-api')
        chalice_stage_config = self.create_chalice_stage_config()
        self.chalice = Chalice(self, 'WebApi', source_dir=web_api_source_dir,
                               stage_config=chalice_stage_config)

        #
        # Users assets
        # Cloudflare manual setup required: add CNAME to DNS i.e. for in me-south-1 region:
        # name: img value: .s3.me-south-1.amazonaws.com
        #
        pyaws_domain = os.environ['PYAWS_CLI_DOMAIN']
        pyaws_image_subdomain = os.environ['PYAWS_CLI_IMAGE_SUBDOMAIN']
        pyaws_img_domain = f"{pyaws_image_subdomain}.{pyaws_domain}"
        img_bucket = Bucket(self, pyaws_img_domain,
                            bucket_name=pyaws_img_domain,
                            public_read_access=False,
                            removal_policy=RemovalPolicy.DESTROY,
                            access_control=BucketAccessControl.AUTHENTICATED_READ,
                            cors=[CorsRule(allowed_methods=[HttpMethods.GET, HttpMethods.POST],
                                           allowed_headers=[],
                                           allowed_origins=[f"https://{pyaws_domain}", "http://localhost:3000"])]
                           )

        img_bucket.add_to_resource_policy(permission=PolicyStatement(
            sid=f"policy.cloudflare.sid.{pyaws_img_domain}",
            effect=Effect.ALLOW,
            principals=[AnyPrincipal()],
            actions=["s3:GetObject"],
            resources=[f"arn:aws:s3:::{pyaws_img_domain}/*"],
            conditions={"IpAddress": {"aws:SourceIp": [
                "103.21.244.0/22",
                "103.22.200.0/22",
                "103.31.4.0/22",
                "108.162.192.0/18",
                "131.0.72.0/22",
                "141.101.64.0/18",
                "162.158.0.0/15",
                "172.64.0.0/13",
                "173.245.48.0/20",
                "188.114.96.0/20",
                "190.93.240.0/20",
                "197.234.240.0/22",
                "198.41.128.0/17",
                "199.27.128.0/21",
                "104.16.0.0/13",
                "104.24.0.0/14"
            ]
            }}
        ))

        BucketDeployment(self, id="assetsDeployment",
                         sources=[Source.asset('./assets')],
                         destination_bucket=img_bucket)


    def create_chalice_stage_config(self):
        """Chalice config for Aws Gateway Stage and Lambda provisioning

        This is used by aws_cdk construct to generate whole stack from chalice app.
        Note: we use ipwhitelist.json for access control
        Note: various env variables injected into lambda and memory config
        """
        PYAWS_CLI_DOMAIN = os.environ['PYAWS_CLI_DOMAIN']
        PYAWS_CLI_AWS_SNS_EMAIL_REGION = os.environ['PYAWS_CLI_AWS_SNS_EMAIL_REGION']
        PYAWS_CLI_IMAGE_SUBDOMAIN = os.environ['PYAWS_CLI_IMAGE_SUBDOMAIN']

        chalice_stage_config = {
            "environment_variables": {
                'DYNAMODB_TABLE_NAME': self.dynamodb_table.table_name,
                "DYNAMODB_STREAM_ARN": self.dynamodb_table.table_stream_arn,
                "PYAWS_CLI_DOMAIN" : PYAWS_CLI_DOMAIN,
                "PYAWS_CLI_AWS_SNS_EMAIL_REGION": PYAWS_CLI_AWS_SNS_EMAIL_REGION,
                "PYAWS_CLI_IMAGE_SUBDOMAIN": PYAWS_CLI_IMAGE_SUBDOMAIN
            },
            'api_gateway_stage': 'v1',
            "api_gateway_policy_file": "ipwhitelist.json",
            'lambda_functions': {
                'lambda_authorizer': {
                    'lambda_memory_size': WebApi._API_HANDLER_LAMBDA_MEMORY_SIZE_1024,
                    'lambda_timeout': WebApi._API_HANDLER_LAMBDA_TIMEOUT_SECONDS,
                    'manage_iam_role': False,
                    'iam_role_arn': self.api_handler_iam_role.role_arn,
                    'reserved_concurrency': 10,
                    'environment_variables': {
                    },
                },
                'api_handler': {
                    'manage_iam_role': False,
                    'iam_role_arn': self.api_handler_iam_role.role_arn,
                    'environment_variables': {
                    },
                    'lambda_memory_size': WebApi._API_HANDLER_LAMBDA_MEMORY_SIZE_1024,
                    'lambda_timeout': WebApi._API_HANDLER_LAMBDA_TIMEOUT_SHORT_SECONDS,
                    'reserved_concurrency': 10
                },
                'periodic_task': {
                    'manage_iam_role': False,
                    'iam_role_arn': self.periodic_task_iam_role.role_arn,
                    'lambda_memory_size': WebApi._API_HANDLER_LAMBDA_MEMORY_SIZE_128,
                    'lambda_timeout': WebApi._API_HANDLER_LAMBDA_TIMEOUT_SHORT_SECONDS,
                    'reserved_concurrency': 2
                },
                'on_table_update': {
                    'manage_iam_role': False,
                    'iam_role_arn': self.on_table_update_iam_role.role_arn,
                    'lambda_memory_size': WebApi._API_HANDLER_LAMBDA_MEMORY_SIZE_128,
                    'lambda_timeout': WebApi._API_HANDLER_LAMBDA_TIMEOUT_SHORT_SECONDS,
                    'reserved_concurrency': 5
                }
            }
        }

        return chalice_stage_config
