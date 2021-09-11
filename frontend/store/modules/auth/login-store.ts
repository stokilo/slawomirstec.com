import {createModule, mutation, action} from "vuex-class-component";
import {$token} from "~/utils/api";
import AuthService from "~/store/api/auth/auth-service"
import Login, {LoginSubmitResult} from "~/store/model/auth/login";


export const VuexModule = createModule({
  namespaced: "login",
  strict: false,
  target: "nuxt",
});

export class LoginStore extends VuexModule {
  authService: AuthService = new AuthService();
  login: Login = new Login();

  @mutation mutateLogin(mutatedLogin: Login) {
    this.login = mutatedLogin;
  }

  @mutation mutateContactReCaptcha(token: string) {
    this.login.recaptcha.token = token
  }

  @mutation clearLoginForm() {
    this.login.email = ""
    this.login.password = ""
  }

  @action
  async onMounted() {
    if (process.env.isDevMode) {
      let loginInitData = new Login();
      loginInitData.email = "test@test.com";
      loginInitData.password = "password123";
      this.mutateLogin(
        loginInitData
      )
    }
  }

  @action
  async onLogin(): Promise<LoginSubmitResult> {
    let loginResult = await this.authService.login(this.login);
    $token.setJwt(loginResult.status.success ? loginResult.auth.jwt : "")
    $token.setRefreshToken(loginResult.status.success ? loginResult.auth.refresh_token : "")
    return loginResult
  }

}

