
export class WithFromJson {

  constructor() {
  }

  fromJson(data: object) {
    Object.assign(this, data);
    return this;
  }

  isObjectWithKey(data: object, key: string) {
    try {
      let obj = {}
      Object.assign(obj, data);
      if (!(key in obj)) {
        return false
      }
    } catch (e) {
      return false;
    }
    return true;
  }
}

export class Status extends WithFromJson {
  public success: boolean;
  public error_code: string;
  public error_message: string;

  constructor(success: boolean = false, error_code: string = "", error_message: string = "") {
    super();
    this.success = success;
    this.error_code = error_code;
    this.error_message = error_message
  }
}

export class FormValidation extends WithFromJson {
  public errors: {[key: string]: Array<string>};
  public passed: boolean;


  constructor(errors: {[key: string]: Array<string>} = {}, passed: boolean = false) {
    super();
    this.errors = errors;
    this.passed = passed;
  }
}

export class Auth extends WithFromJson {
  public jwt: string;
  public refresh_token: string;

  constructor(jwt: string = "", refresh_token: string = "") {
    super();
    this.jwt = jwt;
    this.refresh_token = refresh_token;
  }
}
