import Vue from 'vue'
import { ValidationProvider, ValidationObserver, extend} from 'vee-validate';
import { required, max, min, email } from "vee-validate/dist/rules";

Vue.component('ValidationProvider', ValidationProvider);
Vue.component("ValidationObserver", ValidationObserver);

extend("required", {
  ...required
});

extend("email", {
  ...email
});

extend("max", {
  ...max
});

extend("min", {
  ...min
});
