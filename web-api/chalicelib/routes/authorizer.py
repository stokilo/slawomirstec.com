import jwt
from chalice import Blueprint, AuthResponse
from chalicelib.model.constants import JwtConstants
from chalicelib.dao.auth import AuthDao
from chalicelib.routes.constants import ROUTES_WITH_REQUIRED_AUTH_ALL
from chalicelib import logger
authorizer_blueprint = Blueprint(__name__)


class DenyAuthResponse(AuthResponse):
    """Generate explicit deny policy for lambda authorizer

    This is required because we define ResourcePolicy for API Gateway with explicit
    Allow to certain IP ranges. This conflicts later with unauthorized response from lambda authorizer that is
    also Allow (Allow [] path which is Deny in result). Refer to Table A in AWS doc

    @link https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-authorization-flow.html

    In result request is processed by Api Gateway even if authorizer returns Allow []
    """

    def _generate_policy(self, request):
        allowed_resources = self._generate_allowed_resources(request)
        return {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Deny',
                    'Resource': allowed_resources,
                }
            ]
        }


@authorizer_blueprint.authorizer()
def lambda_authorizer(auth_request):
    """Lambda authorizer for secured routes

    :param auth_request: this is AWS token authorizer, Api Gateway will provide only header with token
    :return: chalice AuthResponse object
    """
    try:
        token = auth_request.token
        payload = jwt.decode(token, verify=False)
        auth_dao = AuthDao()
        existing_user = auth_dao.get_user_by_id(payload['sub'])
        secret = existing_user.secret

        jwt.decode(token, secret, algorithms=['HS256'], options={'require': ['exp', 'iss', 'sub']},
                   audience=JwtConstants.AUD.value)

        return AuthResponse(routes=ROUTES_WITH_REQUIRED_AUTH_ALL, principal_id='user')
    except Exception as e:
        logger.exception(e)
        return DenyAuthResponse(routes=ROUTES_WITH_REQUIRED_AUTH_ALL, principal_id='user')

