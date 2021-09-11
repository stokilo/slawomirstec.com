import {SERVER_API_ROUTES} from "~/store/api/routes";
import SignUp, {SignUpSubmitResult} from "~/store/model/auth/signup";
import Login, {LoginSubmitResult} from "~/store/model/auth/login"
import {Auth, FormValidation, Status} from "~/store/model/shared";
import AxiosService from "~/store/api/axios-service";
import RefreshToken, {RefreshTokenSubmitResult} from "~/store/model/auth/refresh-token";
import {UserProfile, UserProfileSubmitResult} from "~/store/model/profile/user-profile";

export default class AuthService extends AxiosService{

  async signUp(signUp: SignUp) : Promise<SignUpSubmitResult> {
    return super.genericPost(SERVER_API_ROUTES.ROUTE_PATH_AUTH_SIGNUP, signUp, new SignUpSubmitResult(
      new Status(), new FormValidation()
    ))
  }

  async login(login: Login) : Promise<LoginSubmitResult> {
    return super.genericPost(SERVER_API_ROUTES.ROUTE_LOGIN, login, new LoginSubmitResult(
      new Status(), new FormValidation(), new Auth(), new UserProfile()
    ))
  }

  async refreshToken(refreshToken: RefreshToken) : Promise<RefreshTokenSubmitResult> {
    return super.genericPost(SERVER_API_ROUTES.ROUTE_REFRESH_TOKEN, refreshToken, new RefreshTokenSubmitResult(
      new Status(), new Auth()
    ))
  }

  async updateProfile(userProfile: UserProfile) : Promise<UserProfileSubmitResult> {
    return super.genericPost(SERVER_API_ROUTES.ROUTE_PATH_AUTH_PROFILE, userProfile, new UserProfileSubmitResult(
      new UserProfile(), new Status()
    ))
  }

}
