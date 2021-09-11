import ReCaptcha from "~/store/model/recaptcha";
import {Auth, FormValidation, Status, WithFromJson} from "~/store/model/shared";
import {UserProfile} from "~/store/model/profile/user-profile";

export class LoginSubmitResult extends WithFromJson{
  public status: Status
  public formValidation: FormValidation
  public auth: Auth
  public userProfile: UserProfile

  constructor(status: Status, formValidation: FormValidation, auth: Auth, userProfile: UserProfile){
    super()
    this.status = status
    this.formValidation = formValidation
    this.auth = auth
    this.userProfile = userProfile
  }

}

/**
 * Model for login
 */
export default class Login extends WithFromJson{
  public email : string;
  public password: string;
  public recaptcha: ReCaptcha = new ReCaptcha()

  constructor() {
    super()
    this.email = "";
    this.password = "";
  }

  isComplete(): boolean {
    return !!(this.password.length && this.email.length && this.recaptcha.isSet())
  }
}

