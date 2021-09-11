import {extractVuexModule, createProxy} from "vuex-class-component";
import Vuex from "vuex";
import Vue from "vue";
import {SignUpStore} from "~/store/modules/auth/sign-up-store";
import {LoginStore} from "~/store/modules/auth/login-store";
import {ContactStore} from "~/store/modules/profile/contact-store";
import {UserProfileStore} from "~/store/modules/profile/user-profile-store";
import {MenuStore} from "~/store/modules/common/menu-store";
import {TodoStore} from "~/store/modules/app/todo-store";
import {DashboardStore} from "~/store/modules/app/dashboard-store";
import {AppointmentStore} from "~/store/modules/app/appointment-store";

Vue.use(Vuex)

export const store = new Vuex.Store({
  modules: {
    ...extractVuexModule(SignUpStore),
    ...extractVuexModule(LoginStore),
    ...extractVuexModule(ContactStore),
    ...extractVuexModule(MenuStore),
    ...extractVuexModule(TodoStore),
    ...extractVuexModule(DashboardStore),
    ...extractVuexModule(UserProfileStore),
    ...extractVuexModule(AppointmentStore)
  }
});

export const proxy = {
  signUpStoreProxy: createProxy(store, SignUpStore),
  loginStoreProxy: createProxy(store, LoginStore),
  contactStore: createProxy(store, ContactStore),
  menuStore: createProxy(store, MenuStore),
  todoStore: createProxy(store, TodoStore),
  dashboardStore: createProxy(store, DashboardStore),
  userProfileStore: createProxy(store, UserProfileStore),
  appointmentStore: createProxy(store, AppointmentStore)
};
