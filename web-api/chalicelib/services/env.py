import os, subprocess

ENV_DYNAMODB_STREAM_ARN = 'DYNAMODB_STREAM_ARN'
DGB_CHALICE = 'DGB_CHALICE'

def get_dynamodb_stream_arn():
    """Resolve dynamodb stream arn.
    """
    dynamodb_stream_arn = ""
    if ENV_DYNAMODB_STREAM_ARN in os.environ:
        dynamodb_stream_arn = os.environ[ENV_DYNAMODB_STREAM_ARN]
    else:
        # DynamoDb streams are active for 24 hours after deletion of main table
        # We can get a list of streams here, we take first one and we don't check if is ENABLED
        # This is because this is for development chalice run only, on AWS premise it will take
        # stream arn from env variables filled during cdk deployment
        dynamodb_stream_arn = subprocess.run(
            ['aws', 'dynamodbstreams', 'list-streams', '--query', 'Streams[0].StreamArn'],
            stdout=subprocess.PIPE).stdout.decode()

    return dynamodb_stream_arn


def is_chalice_debug_enabled():
    return DGB_CHALICE in os.environ and os.environ[DGB_CHALICE] == "true"