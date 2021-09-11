from enum import Enum
from chalicelib import SSM_PARAMETER_PYAWS_CLI_DOMAIN, SMS_PARAMETER_PYAWS_CLI_AWS_SNS_EMAIL_REGION, PYAWS_CLI_IMAGE_SUBDOMAIN


class AWSConstants(Enum):
    """Constants that are not provided at build time from aws account"""
    SNS_EMAIL_REGION = SMS_PARAMETER_PYAWS_CLI_AWS_SNS_EMAIL_REGION
    SSM_PARAMETER_PYAWS_CLI_DOMAIN = SSM_PARAMETER_PYAWS_CLI_DOMAIN
    PYAWS_CLI_IMAGE_SUBDOMAIN = PYAWS_CLI_IMAGE_SUBDOMAIN
    SNS_EMAIL_VERIFIED_SENDER = "your-verified-sender@gmail.com"


class ErrorCode(Enum):
    """All unique error code types that can be returned by the API"""

    # default
    NONE = "",
    GENERIC_ERROR = "generic-error"
    FORM_PROCESSING_ERROR = "form-processing-error"


class JwtConstants(Enum):

    JWT_JTI = "pyaws_v1"
    REFRESH_TOKEN_JTI = "pyaws_rt_v1"

    JWT_VALID_SECONDS = 600,
    REFRESH_TOKEN_VALID_SECONDS = 1200,

    AUD = f"www.{SSM_PARAMETER_PYAWS_CLI_DOMAIN}"
    ISS = f"sso.{SSM_PARAMETER_PYAWS_CLI_DOMAIN}"



