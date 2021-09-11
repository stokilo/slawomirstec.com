import jwt
from contextvars import ContextVar
from typing import TypeVar

T = TypeVar('T')

REQUEST_SCOPE = ContextVar('request_scope')


class Request():
    """Chalice request wrapper available in context of lambda execution, you can import REQUEST_SCOPE
    into your services and have an access into chalice specific request parameters i.e. headers, user language etc
    """
    chalice_request: any
    headers: dict

    # UI language
    lang_header: str = "X-Language"
    default_language: str = "en"

    # JWT authenticated user id
    auth_header: str = "Authorization"
    auth_client_id: str = None

    def __init__(self, chalice_request):
        self.chalice_request = chalice_request
        self.headers = chalice_request.headers
        self.read_user_id()

    def language(self):
        if self.lang_header in self.headers:
            return self.headers[self.lang_header]
        else:
            return self.default_language

    def read_user_id(self):
        if self.auth_header in self.headers:
            auth_token = self.headers[self.auth_header]
            payload = jwt.decode(auth_token, verify=False)
            self.auth_client_id = payload['sub']