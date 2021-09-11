import bcrypt
import uuid
import jwt
from datetime import datetime, timedelta
from chalicelib.dao.auth import UserEntity, UserProfile
from chalicelib.dao.auth import AuthDao
from chalicelib.i18n import ta
from chalicelib.model.auth import SignUpModel, LoginModel, RefreshTokenModel, SignUpSubmitResult, SignUpFormValidation, \
    LoginSubmitResult, LoginFormValidation, RefreshTokenSubmitResult, UserProfileModel, UserProfileUpdateResult
from chalicelib.model.constants import ErrorCode, JwtConstants
from chalicelib.model.shared import Status, Auth
from chalicelib import logger, REQUEST_SCOPE


class AuthService:
    def __init__(self) -> None:
        self.auth_dao = AuthDao()

    def handle_sign_up(self, sign_up_model: SignUpModel) -> SignUpSubmitResult:
        """Handle user sign up request
        """
        result = SignUpSubmitResult(SignUpFormValidation(), Status())
        try:
            result.formValidation.validate_signup(sign_up_model)
            if not result.formValidation.passed:
                return result

            if self.auth_dao.has_user_with_email(sign_up_model.email):
                result.status.error(ErrorCode.FORM_PROCESSING_ERROR, ta("user.already.exists"))
                return result

            password_hashed = bcrypt.hashpw(sign_up_model.password.encode('utf8'), bcrypt.gensalt()).decode('utf-8')
            self.auth_dao.create_user(sign_up_model.email, password_hashed, str(uuid.uuid4()), str(uuid.uuid4()))
            result.status.success = True
        except Exception as e:
            logger.exception(e)
            result.status.generic_error()
        return result

    def handle_login(self, login_model: LoginModel) -> LoginSubmitResult:
        """Handle user login request"""

        result = LoginSubmitResult(LoginFormValidation(), Status(), Auth(), UserProfileModel())
        try:
            result.formValidation.validate_login(login_model)
            if not result.formValidation.passed:
                return result

            users = self.auth_dao.get_users_by_email(login_model.email)
            if len(users) != 1 or users[0].email.lower() != login_model.email.lower():
                result.status.error(ErrorCode.FORM_PROCESSING_ERROR, ta("user.not.found"))
                return result

            user = users[0]
            if bcrypt.checkpw(login_model.password.encode("utf-8"), user.password.encode('utf-8')):
                (result.auth.jwt, result.auth.refresh_token) = self.generate_tokens(user.user_id,
                                                                                    user.secret,
                                                                                    user.secret_refresh_token)
                result.status.success = True
                result.userProfile.firstName = user.user_profile.firstName
                result.userProfile.lastName = user.user_profile.lastName
                result.userProfile.profileImagePath = user.user_profile.profileImagePath
            else:
                result.status.error(ErrorCode.FORM_PROCESSING_ERROR, ta("invalid.password"))
                return result

        except Exception as e:
            logger.exception(e)
            result.status.generic_error()
        return result

    def handle_refresh_token(self, refresh_token_model: RefreshTokenModel) -> RefreshTokenSubmitResult:
        """Handle refresh token"""

        result = RefreshTokenSubmitResult(Status(), Auth())
        try:
            if not refresh_token_model.refreshToken:
                return result

            payload = jwt.decode(refresh_token_model.refreshToken, verify=False)
            user_id = payload["sub"]
            user = self.auth_dao.get_user_by_id(user_id)
            if not user:
                logger.debug(f"Could not find the uses associated with "
                              f"the jwt token: {refresh_token_model.refreshToken}, skipping...")
                return result

            # Validate refresh token, must be valid at time of calling refresh
            payload = jwt.decode(refresh_token_model.refreshToken, user.secret_refresh_token,
                       algorithms=['HS256'], options={'require': ['exp', 'iss', 'sub'], 'verify_nbf': False},
                       audience=JwtConstants.AUD.value)

            # Assume token is valid, generate new secrets, tokens and update secrets in db
            new_secret = str(uuid.uuid4())
            new_secret_refresh_token = str(uuid.uuid4())
            (jwt_token, refresh_token) = self.generate_tokens(user.user_id, new_secret, new_secret_refresh_token)
            updated = self.auth_dao.update(user, [
                UserEntity.secret.set(new_secret),
                UserEntity.secret_refresh_token.set(new_secret_refresh_token)
            ])
            if updated:
                result.auth.jwt = jwt_token
                result.auth.refresh_token = refresh_token
                result.status.success = True

        except Exception as e:
            logger.exception(e)
            return result
        return result

    @staticmethod
    def generate_tokens(subject: str, jwt_secret: str, refresh_token_secret: str):
        """Generate two JWT tokens

        Secrets are stored for each user in database. Both are different.
        Both tokens are valid for different amount of time.
        Subject is unique id of the user.
        """
        utc_now = int(datetime.utcnow().timestamp())
        payload = {
            'iss': JwtConstants.ISS.value,
            "sub": subject,
            'aud': JwtConstants.AUD.value,
            'exp': datetime.utcnow() + timedelta(seconds=int(JwtConstants.JWT_VALID_SECONDS.value[0])),
            'iat': utc_now,
            'jti': JwtConstants.JWT_JTI.value
        }

        payload_refresh_token = {
            'iss': JwtConstants.ISS.value,
            "sub": subject,
            'aud': JwtConstants.AUD.value,
            'exp': datetime.utcnow() + timedelta(seconds=int(JwtConstants.REFRESH_TOKEN_VALID_SECONDS.value[0])),
            'iat': utc_now,
            'jti': JwtConstants.REFRESH_TOKEN_JTI.value
        }

        jwt_token = jwt.encode(payload, jwt_secret, algorithm='HS256').decode('utf-8')
        refresh_token = jwt.encode(payload_refresh_token, refresh_token_secret, algorithm='HS256').decode('utf-8')

        return jwt_token, refresh_token

    def handle_user_profile_update(self, user_profile_model: UserProfileModel) -> UserProfileUpdateResult:
        """Handle user profile update
        """
        result = UserProfileUpdateResult(Status(), user_profile_model)
        try:
            client_id = REQUEST_SCOPE.get().auth_client_id
            user = self.auth_dao.get_user_by_id(client_id)

            user_profile = UserProfile()
            user_profile.firstName = user_profile_model.firstName
            user_profile.lastName = user_profile_model.lastName
            user_profile.profileImagePath = user_profile_model.profileImagePath

            self.auth_dao.update(
               entity=user,
               actions=[UserEntity.user_profile.set(user_profile)]
            )

            result.status.success = True
        except Exception as e:
            logger.exception(e)
            result.status.generic_error()
        return result

authService = AuthService()
