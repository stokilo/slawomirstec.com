/**
 * Model for contact form
 */
import ReCaptcha from "~/store/model/recaptcha";
import {Status, FormValidation, WithFromJson} from "~/store/model/shared"

export class ContactModelSubmitResult extends WithFromJson{
   public contactModel: Contact
   public status: Status
   public formValidation: FormValidation

  constructor(contactModel: Contact, status: Status, formValidation: FormValidation) {
    super()
    this.contactModel = contactModel
    this.status = status
    this.formValidation = formValidation
  }

}

export class Contact extends WithFromJson{
  public name : string
  public email : string
  public details : string
  public recaptcha: ReCaptcha = new ReCaptcha()

  constructor(name: string = "", email: string = "", details = "") {
    super()
    this.name = name
    this.email = email
    this.details = details
  }

  isComplete(): boolean {
    return !!(this.name.length && this.email.length && this.details.length && this.recaptcha.isSet())
  }

}

