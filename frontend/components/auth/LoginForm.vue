<template>
  <div>
    <div>
      <div role="alert" class="alert alert-danger" :hidden="loginErrorMessage.length <= 0">
        {{ loginErrorMessage }}
      </div>


      <ValidationObserver ref="form" v-slot="{ invalid }">
        <form id="rulesForm" class="tooltip-label-right" novalidate @submit.prevent="onSend">
          <fieldset :disabled="isFormDisabled">

            <ValidationProvider v-slot="v" rules="required|email|min:3|max:250" vid="email">
              <label class="form-group has-float-label mb-4">
                <input type="text" maxlength="249" class="form-control" name="email" v-model="loginStore.login.email">
                <span>{{ $t('login-form.email') }}</span>
              </label>
              <span class="form-text text-danger">{{ v.errors[0] }}</span>
              <br/>
            </ValidationProvider>

            <ValidationProvider v-slot="v" rules="required|min:7|max:250" vid="password">
              <label class="form-group has-float-label mb-4">
                <input type="password" maxlength="249" class="form-control" name="password"
                       v-model="loginStore.login.password">
                <span>{{ $t('login-form.password') }}</span>
              </label>
              <span class="form-text text-danger">{{ v.errors[0] }}</span>
              <br/>
            </ValidationProvider>

            <ValidationProvider v-slot="v" rules="required">
              <recaptcha
                @error="onReCaptchaError"
                @success="onReCaptchaSuccess"
                @expired="onReCaptchaExpired"
              />
              <span class="form-text text-danger">{{ v.errors[0] }}</span>
            </ValidationProvider>
          </fieldset>
          <div class="p-3 text-center">
            <button class="btn btn-primary btn-lg btn-shadow" :disabled="invalid || !isFormFilled">Login</button>
          </div>
        </form>
      </ValidationObserver>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import {proxy} from "~/store/store";
import Component from "vue-class-component";
import {LoginStore} from "~/store/modules/auth/login-store";
import {NuxtJsRouteHelper} from "~/store/api/routes";
import {$i18n, $loader, $notify} from "~/utils/api";
import {UserProfileStore} from "~/store/modules/profile/user-profile-store";

@Component
export default class LoginForm extends Vue {
  loginStore: LoginStore = proxy.loginStoreProxy
  userProfileStore: UserProfileStore = proxy.userProfileStore
  isFormDisabled: boolean = false
  loginErrorMessage: string = ""

  mounted() {
    this.loginStore.onMounted()
  }

  get isFormFilled() {
    return this.loginStore.login.isComplete() || process.env.isDevMode
  }

  async onSend() {
    this.isFormDisabled = true
    let loader = $loader.show()

    try {

      if (this.loginStore.login.recaptcha.isSet() || process.env.isDevMode) {
        let loginResult = await this.loginStore.onLogin();

        if (!loginResult.formValidation.passed) {
          //@ts-ignore
          this.$refs.form.setErrors(
            loginResult.formValidation.errors
          );
        }

        // general error message for form processing
        if (!loginResult.status.success) {
          this.loginErrorMessage = loginResult.status.error_message
        } else {
          this.$router.push(NuxtJsRouteHelper.getDefaultAppRoute())
          this.loginStore.clearLoginForm()
          this.userProfileStore.mutateUserProfile(loginResult.userProfile)
        }
      }

      // @ts-ignore
      await this.$recaptcha.reset()
    } catch (err) {
      $notify("error", $i18n.t("api.error-msg-title"), $i18n.t("api.error-msg-content"));
    }
    this.loginStore.mutateContactReCaptcha("")
    this.isFormDisabled = false
    setTimeout(() => {
      loader.hide()
    }, 400)
  }


  onReCaptchaError(error: any) {
    this.loginStore.mutateContactReCaptcha("");
  }

  onReCaptchaSuccess(token: string) {
    this.loginStore.mutateContactReCaptcha(token)
  }

  onReCaptchaExpired() {
    this.loginStore.mutateContactReCaptcha("");
  }

}

</script>
