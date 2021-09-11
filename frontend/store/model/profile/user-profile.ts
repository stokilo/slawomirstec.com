/**
 * Model for user profile
 */
import {Status, WithFromJson} from "~/store/model/shared"

export class UserProfile extends WithFromJson{
  public firstName : string
  public lastName : string
  public profileImagePath : string

  constructor(firstName: string = "", lastName: string = "", profileImagePath: string = "") {
    super();
    this.firstName = firstName;
    this.lastName = lastName;
    this.profileImagePath = profileImagePath;
  }
}

export class UserProfileSubmitResult extends WithFromJson{
  public userProfile: UserProfile
  public status: Status

  constructor(userProfile: UserProfile, status: Status) {
    super();
    this.userProfile = userProfile;
    this.status = status;
  }
}
