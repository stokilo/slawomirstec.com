<template>
  <div class="card mb-4">
    <div class="card-body" :hidden="isContactSend">
      <h2 class="mb-4">{{ $t('contact-form.contact-me') }}</h2>
      <div role="alert" class="alert alert-danger" :hidden="contactSendErrorMessage.length <= 0">
        {{ contactSendErrorMessage }}
      </div>
      <br/>
      <ValidationObserver ref="form" v-slot="{ invalid }">

        <form id="rulesForm" class="tooltip-label-right" novalidate @submit.prevent="onSend">
          <fieldset :disabled="isFormDisabled">

            <ValidationProvider v-slot="v" rules="required|min:5|max:250" vid="name">
              <div class="form-group position-relative error-l-50">
                <label>{{ $t('contact-form.name') }}</label>
                <input type="text" maxlength="249" class="form-control" name="name" v-model="contactStore.contact.name">
                <span class="form-text text-danger">{{ v.errors[0] }}</span>
              </div>
            </ValidationProvider>

            <ValidationProvider v-slot="v" rules="required|email|min:3|max:250" vid="email">
              <div class="form-group position-relative error-l-50">
                <label>{{ $t('contact-form.email') }}</label>
                <input type="text" maxlength="249" class="form-control" name="email"
                       v-model="contactStore.contact.email">
                <span class="form-text text-danger">{{ v.errors[0] }}</span>
              </div>
            </ValidationProvider>

            <ValidationProvider v-slot="v" rules="required|min:5|max:250" vid="details">
              <div class="form-group position-relative error-l-50" vid="details">
                <label>{{ $t('contact-form.details') }}</label>
                <textarea class="form-control" maxlength="249" rows="2" name="details"
                          v-model="contactStore.contact.details"></textarea>
                <span class="form-text text-danger">{{ v.errors[0] }}</span>
              </div>
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
          <br/>

          <button class="btn btn-primary mb-0" :disabled="invalid || !isFormFilled">Send</button>
        </form>
      </ValidationObserver>
    </div>

    <div class="alert alert-success" role="alert" :hidden="!isContactSend">
      <span>{{ $t('contact-form.success') }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import {proxy} from "~/store/store";
import {ContactStore} from "~/store/modules/profile/contact-store";
import {$i18n, $loader, $notify} from "~/utils/api";
@Component
export default class ContactForm extends Vue {
  contactStore: ContactStore = proxy.contactStore;
  isFormDisabled: boolean = false
  isContactSend: boolean = false
  contactSendErrorMessage: string = ""

  mounted() {
    this.contactStore.onMounted()
  }

  get isFormFilled() {
    return this.contactStore.contact.isComplete() || process.env.isDevMode
  }

  async onSend() {
    this.isFormDisabled = true
    let loader = $loader.show()

    try {
      if (this.contactStore.contact.recaptcha.isSet() || process.env.isDevMode) {
        let contactSaveResult = await this.contactStore.onSaveContact();

        if (contactSaveResult.status.success) {
          this.isContactSend = true
        }

        // specific form field errors
        if (!contactSaveResult.formValidation.passed) {
          //@ts-ignore
          this.$refs.form.setErrors(
            contactSaveResult.formValidation.errors
          );
        }

        // general error message for form processing
        if (!contactSaveResult.status.success) {
          this.contactSendErrorMessage = contactSaveResult.status.error_message
        }
      }
      // @ts-ignore
      await this.$recaptcha.reset()
    } catch (err) {
      $notify("error", $i18n.t("api.error-msg-title"), $i18n.t("api.error-msg-content"));
    }

    this.contactStore.mutateContactReCaptcha("")
    this.isFormDisabled = false
    setTimeout(() => {
      loader.hide()
    }, 400)
  }

  onReCaptchaError(error: any) {
    this.contactStore.mutateContactReCaptcha("");
  }

  onReCaptchaSuccess(token: string) {
    this.contactStore.mutateContactReCaptcha(token)
  }

  onReCaptchaExpired() {
    this.contactStore.mutateContactReCaptcha("");
  }
}
</script>

