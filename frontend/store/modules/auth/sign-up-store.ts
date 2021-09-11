import {createModule, mutation, action} from "vuex-class-component";
import SignUp from "~/store/model/auth/signup";
import AuthService from "~/store/api/auth/auth-service"

export const VuexModule = createModule({
  namespaced: "signUp",
  strict: false,
  target: "nuxt",
});

export class SignUpStore extends VuexModule {
  authService: AuthService = new AuthService();
  signUp: SignUp = new SignUp();

  @mutation mutateSignUp(mutatedSignUp: SignUp) {
    this.signUp = mutatedSignUp;
  }

  @mutation mutateContactReCaptcha(token: string) {
    this.signUp.recaptcha.token = token
  }

  @action
  async onMounted() {
    if (process.env.isDevMode) {
      let signUpInitData = new SignUp();
      signUpInitData.password = "test";
      signUpInitData.email = "test@test.com";
      this.mutateSignUp(
        signUpInitData
      )
    }
  }

  @action
  async onSignUp() {
    return await this.authService.signUp(this.signUp);
  }

}

