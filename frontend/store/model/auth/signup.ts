import {FormValidation, Status, WithFromJson} from "~/store/model/shared";
import ReCaptcha from "~/store/model/recaptcha";


export class SignUpSubmitResult extends WithFromJson{
  public status: Status
  public formValidation: FormValidation

  constructor(status: Status, formValidation: FormValidation) {
    super()
    this.status = status
    this.formValidation = formValidation
  }

}

/**
 * Model for signup.
 */
export default class SignUp extends WithFromJson{
  public password: string;
  public email: string;
  public recaptcha: ReCaptcha = new ReCaptcha()

  constructor() {
    super()
    this.password = "";
    this.email = "";
  }

  isComplete(): boolean {
    return !!(this.password.length && this.email.length && this.recaptcha.isSet())
  }

}
