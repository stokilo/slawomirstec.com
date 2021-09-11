import Vue from 'vue'
import VueI18n from 'vue-i18n'
import { initializeI18n } from '~/utils/api'
import validationMessagesEn from '~/node_modules/vee-validate/dist/locale/en';
import validationMessagesPl from '~/node_modules/vee-validate/dist/locale/pl';
import { configure } from 'vee-validate';

Vue.use(VueI18n);

let en = require('~/locales/en.json')
en.validations = validationMessagesEn

let pl = require('~/locales/pl.json')
pl.validations = validationMessagesPl

export default ({ app }, inject) => {
  app.i18n = new VueI18n({
    locale: 'en',
    fallbackLocale: 'en',
    messages: {
      en: en
    }
  });

  //conversion filter for date values received from python backend
  Vue.filter('formatPDate', function(value) {
    if (value) {
      let vDate = new Date(value * 1000)
      return `${vDate.toLocaleDateString('en-us')} ${vDate.toLocaleTimeString('en-us')}`
    }
  });

  //see https://logaretm.github.io/vee-validate/guide/localization.html#vue-i18n
  //it tells vee-validate to search for translations defined for i18n
  configure({
    defaultMessage: (field, values) => {
      values._field_ = app.i18n.t(`fields.${field}`);
      return app.i18n.t(`validations.messages.${values._rule_}`, values);
    }
  });

  initializeI18n(app.i18n);
}


