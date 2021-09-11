import {createModule, mutation} from "vuex-class-component";
import {UserProfile} from "~/store/model/profile/user-profile";

export const VuexModule = createModule({
  namespaced: "userProfile",
  strict: false,
  target: "nuxt",
});

export class UserProfileStore extends VuexModule {
  userProfile: UserProfile = new UserProfile()

  @mutation mutateUserProfile(mutatedUserProfile: UserProfile) {
    this.userProfile = mutatedUserProfile
  }

  get fullName(): string {
    return this.userProfile.firstName + ' ' + this.userProfile.lastName
  }

  get profileImgUrl(): string {
    let url = process.env.isDevMode ? "https://img.your-domain.com" : process.env.nuxtBaseUrlImageCdn
    return `${url}/${this.userProfile.profileImagePath}`
  }

}

