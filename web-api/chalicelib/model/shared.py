from dataclasses import dataclass
from dataclasses_json import dataclass_json
from chalicelib.model.constants import ErrorCode
from chalicelib.i18n import te


@dataclass_json
@dataclass
class Status:
    """Status of processing of the request
    """
    success: bool = False
    error_code: ErrorCode = ErrorCode.NONE
    error_message: str = ""

    def error(self, error_code: ErrorCode, error_message: str):
        self.error_code = error_code
        self.error_message = error_message

    def generic_error(self):
        self.error_code = ErrorCode.GENERIC_ERROR
        self.error_message = te("generic.error")


@dataclass_json
@dataclass
class Auth:
    """Auth data for the request
    """
    jwt: str = ""
    refresh_token: str = ""


@dataclass_json
@dataclass
class OnlyStatus:
    """Responses that only return status
    """
    status: Status = Status()
