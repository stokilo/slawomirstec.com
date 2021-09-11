from chalice import Blueprint, Response

from chalicelib.routes.authorizer import lambda_authorizer
from chalicelib.services.auth import authService
from chalicelib.routes.constants import *
from chalicelib.model.auth import SignUpModel, LoginModel, RefreshTokenModel, UserProfileModel

auth_routes = Blueprint(__name__)


@auth_routes.route(ROUTE_PATH_AUTH_SIGNUP, methods=['POST'])
def register() -> Response:
    sign_up_model = SignUpModel.from_json(auth_routes.current_request.raw_body)
    signup_result = authService.handle_sign_up(sign_up_model)
    if signup_result.status.success:
        return Response(signup_result.to_json())

    return Response(signup_result.to_json(), {}, 500)


@auth_routes.route(ROUTE_PATH_AUTH_LOGIN, methods=['POST'])
def register() -> Response:
    login_model = LoginModel.from_json(auth_routes.current_request.raw_body)
    login_result = authService.handle_login(login_model)
    if login_result.status.success:
        return Response(login_result.to_json())

    return Response(login_result.to_json(), {}, 500)


@auth_routes.route(ROUTE_PATH_REFRESH_TOKEN, methods=['POST'])
def register() -> Response:
    refresh_token_model = RefreshTokenModel.from_json(auth_routes.current_request.raw_body)
    refresh_token_result = authService.handle_refresh_token(refresh_token_model)
    if refresh_token_result.status.success:
        return Response(refresh_token_result.to_json())

    return Response(refresh_token_result.to_json(), {}, 401)

@auth_routes.route(ROUTE_PROFILE, methods=['POST'], authorizer=lambda_authorizer)
def register() -> Response:
    user_profile_model = UserProfileModel.from_json(auth_routes.current_request.raw_body)
    user_profile_update_result = authService.handle_user_profile_update(user_profile_model)
    if user_profile_update_result.status.success:
        return Response(user_profile_update_result.to_json())

    return Response(user_profile_update_result.to_json(), {}, 500)