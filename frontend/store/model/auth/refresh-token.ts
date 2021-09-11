import {Auth, Status, WithFromJson} from "~/store/model/shared";

export class RefreshTokenSubmitResult extends WithFromJson{
  public status: Status
  public auth: Auth

  constructor(status: Status, auth: Auth){
    super()
    this.status = status
    this.auth = auth
  }

}

/**
 * Model for refresh token request
 */
export default class RefreshToken extends WithFromJson{
  public refreshToken : string;

  constructor(refreshToken: string) {
    super()
    this.refreshToken = refreshToken;
  }
}

