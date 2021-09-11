/**
 * Model for upload functionality
 */
import {Status, WithFromJson} from "~/store/model/shared"

export class UploadObjectField {
  public key: string
  public policy: string
  public 'x-amz-algorithm': string
  public 'x-amz-credential': string
  public 'x-amz-date': string
  public 'x-amz-signature': string

  constructor(key: string = "", policy: string = "", x_amz_algorithm: string = "", x_amz_credential: string = "",
              x_amz_date: string = "", x_amz_signature: string = "") {
    this.key = key;
    this.policy = policy;
    this["x-amz-algorithm"] = x_amz_algorithm;
    this["x-amz-credential"] = x_amz_credential;
    this["x-amz-date"] = x_amz_date;
    this["x-amz-signature"] = x_amz_signature;
  }
}

export class UploadObject {
  public url: string
  public fields: UploadObjectField

  constructor(url: string, fields: UploadObjectField) {
    this.url = url;
    this.fields = fields;
  }
}

export class SignedUploadUrlGetResult extends WithFromJson{
  public upload: UploadObject
  public status: Status

  constructor(upload: UploadObject, status: Status) {
    super();
    this.upload = upload
    this.status = status;
  }
}



