<template>
  <div>
    <div :hidden="isSubmitSuccessful">
      <div role="alert" class="alert alert-danger" :hidden="signUpErrorMessage.length <= 0">
        {{ signUpErrorMessage }}
      </div>


      <ValidationObserver ref="form" v-slot="{ invalid }">
        <form id="rulesForm" class="tooltip-label-right" novalidate @submit.prevent="onSend">
          <fieldset :disabled="isFormDisabled">

            <ValidationProvider v-slot="v" rules="required|email|min:3|max:250" vid="email">
              <label class="form-group has-float-label mb-4">
                <input type="text" maxlength="249" class="form-control" name="email" v-model="signUpStore.signUp.email">
                <span>{{ $t('signup-form.email') }}</span>
              </label>
              <span class="form-text text-danger">{{ v.errors[0] }}</span>
              <br/>
            </ValidationProvider>

            <ValidationProvider v-slot="v" rules="required|min:7|max:250" vid="password">
              <label class="form-group has-float-label mb-4">
                <input type="password" maxlength="249" class="form-control" name="password"
                       v-model="signUpStore.signUp.password">
                <span>{{ $t('signup-form.password') }}</span>
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
            <button class="btn btn-primary btn-lg btn-shadow" :disabled="invalid || !isFormFilled">Register</button>
          </div>
        </form>
      </ValidationObserver>
    </div>
    <div class="alert alert-success" role="alert" :hidden="!isSubmitSuccessful">
      <span>{{ $t('signup-form.success') }}</span>
      <NuxtLink to="/login">{{ $t("signup-form.login-link") }}</NuxtLink>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import {proxy} from "~/store/store";
import {SignUpStore} from "~/store/modules/auth/sign-up-store";
import Component from "vue-class-component";
import {$i18n, $loader, $notify} from "~/utils/api";

@Component
export default class SignUpForm extends Vue {
  signUpStore: SignUpStore = proxy.signUpStoreProxy
  isFormDisabled: boolean = false
  isSubmitSuccessful: boolean = false
  signUpErrorMessage: string = ""

  mounted() {
    this.signUpStore.onMounted()
  }

  get isFormFilled() {
    return this.signUpStore.signUp.isComplete() || process.env.isDevMode
  }

  async onSend() {
    this.isFormDisabled = true
    let loader = $loader.show()

    try {
      if (this.signUpStore.signUp.recaptcha.isSet() || process.env.isDevMode) {
        let signUpResult = await this.signUpStore.onSignUp();

        if (signUpResult.status.success) {
          this.isSubmitSuccessful = true
        }

        if (!signUpResult.formValidation.passed) {
          //@ts-ignore
          this.$refs.form.setErrors(
            signUpResult.formValidation.errors
          );
        }

        // general error message for form processing
        if (!signUpResult.status.success) {
          this.signUpErrorMessage = signUpResult.status.error_message
        }
      }
      // @ts-ignore
      await this.$recaptcha.reset()
    } catch (err) {
      $notify("error", $i18n.t("api.error-msg-title"), $i18n.t("api.error-msg-content"));
    }

    this.signUpStore.mutateContactReCaptcha("")
    this.isFormDisabled = false
    setTimeout(() => {
      loader.hide()
    }, 400)
  }


  onReCaptchaError(error: any) {
    this.signUpStore.mutateContactReCaptcha("");
  }

  onReCaptchaSuccess(token: string) {
    this.signUpStore.mutateContactReCaptcha(token)
  }

  onReCaptchaExpired() {
    this.signUpStore.mutateContactReCaptcha("");
  }

}

</script>
