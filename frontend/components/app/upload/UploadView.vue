<template>
  <div class="disable-text-selection">
    <form id="rulesForm" class="tooltip-label-right" novalidate>

      <ValidationProvider v-slot="v" rules="required|max:250" vid="firstName">
        <label class="form-group has-float-label mb-4">
          <input type="text" maxlength="249" class="form-control" name="firstName"
                 v-model="userProfileStore.userProfile.firstName">
          <span>{{ $t('upload.first-name') }}</span>
        </label>
        <span class="form-text text-danger">{{ v.errors[0] }}</span>
        <br/>
      </ValidationProvider>

      <ValidationProvider v-slot="v" rules="required|max:250" vid="lastName">
        <label class="form-group has-float-label mb-4">
          <input type="text" maxlength="249" class="form-control" name="lastName"
                 v-model="userProfileStore.userProfile.lastName">
          <span>{{ $t('upload.last-name') }}</span>
        </label>
        <span class="form-text text-danger">{{ v.errors[0] }}</span>
        <br/>
      </ValidationProvider>

      <label class="form-group mb-4 warning">
        <span>{{ $t('upload.select-file') }}</span>
      </label>
      <b-input-group class="mb-3">
        <b-input-group-prepend>
          <b-button variant="outline-secondary" :disabled="!isFileSelected" @click="onUploadAndSave">
            {{ $t('upload.upload-label') }}
          </b-button>
        </b-input-group-prepend>
        <b-form-file v-model="file" ref="fileinput" accept=".png" :placeholder="$t('upload.choose-file')"></b-form-file>
      </b-input-group>
    </form>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import UploadService from "~/store/api/app/upload-service";
import {UserProfileStore} from "~/store/modules/profile/user-profile-store";
import {proxy} from "~/store/store";
import {UserProfile} from "~/store/model/profile/user-profile";
import {$i18n, $loader, $notify} from "~/utils/api";
import AuthService from "~/store/api/auth/auth-service";

@Component({
  head: {bodyAttrs: {class: "rounded"}}
})
export default class UploadViewComponent extends Vue {
  userProfileStore: UserProfileStore = proxy.userProfileStore
  uploadService: UploadService = new UploadService()
  authService: AuthService = new AuthService();
  file: File = new File([], "");

  async onUploadAndSave() {
    let loader = $loader.show()
    try {
      let signedUploadUrl = await this.uploadService.getSignedUploadUrl()
      //@ts-ignore
      const data = Object.entries(signedUploadUrl.upload.fields).reduce((fd, [key, val]) => (fd.append(key, val), fd),
        new FormData())
      data.append('file', this.file)

      await this.uploadService.uploadS3Post(signedUploadUrl, data)

      let userProfile = new UserProfile(this.userProfileStore.userProfile.firstName,
        this.userProfileStore.userProfile.lastName, signedUploadUrl.upload.fields.key)
      let userProfileUpdateResult = await this.authService.updateProfile(userProfile)

      if (userProfileUpdateResult.status.success) {
        this.userProfileStore.mutateUserProfile(userProfile)
        $notify("success", $i18n.t("api.update-status-msg-title"), $i18n.t("upload.upload-ok"));
      } else {
        $notify("error", $i18n.t("api.error-msg-title"), $i18n.t("upload.upload-failed"));
      }

    } catch (e) {
      $notify("error", $i18n.t("api.error-msg-title"), $i18n.t("upload.upload-failed"));
    }

    setTimeout(() => {
      loader.hide()
    }, 400)
  }

  get isFileSelected() {
    return this.userProfileStore.userProfile.lastName.length > 0 &&
      this.userProfileStore.userProfile.firstName.length > 0 &&
      this.file.name.length > 0;
  }
}
</script>

