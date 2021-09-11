import VueNotify from "~/components/common/notification/Notify"
import Vue from 'vue'
import {initializeNotify} from "~/utils/api";

export default ({ app }, inject) => {
  let Constr = Vue.extend(VueNotify)
  let Notify = new Constr()
  Notify.options = Object.assign(Notify.options, { duration: 3000, permanent: false })
  let vm = Notify.$mount()
  document.querySelector('body').appendChild(vm.$el)
  Vue.notify = Vue.prototype.$notify = (type = 'success', title, message, options = {}) => {
    Notify.addItem(type, title, message, options)
  }

  app.$notify = Vue.notify
  initializeNotify(app.$notify);
}

