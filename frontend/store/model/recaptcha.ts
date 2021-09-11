/**
 * Model for capturing recaptcha
 */
export default class ReCaptcha {
  public token : string;

  constructor() {
    this.token = "";
  }

  isSet(): boolean {
    return !!(this.token && this.token.length)
  }

}

