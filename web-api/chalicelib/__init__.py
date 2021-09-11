import logging
import os
from chalice import Chalice, ConvertToMiddleware
from aws_lambda_powertools import Logger

from chalicelib.model.request import REQUEST_SCOPE, Request

app = Chalice(app_name='pyaws-api')
app.log.setLevel(logging.INFO)

# power tools logger with interface to run before each route and decorate logger metadata with shared parameters
# here we use user id and include with each logged in message, this helps to inspect logs
logger = Logger(service="pyaws")
app.register_middleware(ConvertToMiddleware(logger.inject_lambda_context))


@app.middleware('http')
def decorate_http_calls(event, get_response):
    try:
        REQUEST_SCOPE.set(Request(event))
        logger.info(f"Handle: {event.path}")
        logger.structure_logs(append=True, client_id=REQUEST_SCOPE.get().auth_client_id)
    except Exception as e:
        logger.error(e)
    return get_response(event)

# this domain is filled from .secret.config.yaml
SSM_PARAMETER_PYAWS_CLI_DOMAIN = ""
# aws region used for email sending from .secret.config.yaml, MENA regions is not offering this service
# so we have to configure it
SMS_PARAMETER_PYAWS_CLI_AWS_SNS_EMAIL_REGION = ""
PYAWS_CLI_IMAGE_SUBDOMAIN = ""

# in development we don't have AWS_ACCESS_KEY_ID provided, it is available only on aws premise
if "AWS_ACCESS_KEY_ID" in os.environ:
    SSM_PARAMETER_PYAWS_CLI_DOMAIN = os.environ['PYAWS_CLI_DOMAIN']
    SMS_PARAMETER_PYAWS_CLI_AWS_SNS_EMAIL_REGION = os.environ['PYAWS_CLI_AWS_SNS_EMAIL_REGION']
    PYAWS_CLI_IMAGE_SUBDOMAIN = os.environ['PYAWS_CLI_IMAGE_SUBDOMAIN']
else:
    SMS_PARAMETER_PYAWS_CLI_AWS_SNS_EMAIL_REGION = "us-east-2"
    PYAWS_CLI_IMAGE_SUBDOMAIN = "img"
    SSM_PARAMETER_PYAWS_CLI_DOMAIN = "your-domain.com"
