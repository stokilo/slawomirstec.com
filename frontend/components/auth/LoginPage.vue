<template>
  <div>
    <div class="fixed-background"></div>
    <main>
      <div class="container">
        <div class="row h-100">
          <div class="col-12 col-md-10 mx-auto my-auto">
            <div class="card auth-card">
              <div class="position-relative image-side ">
                <p class=" text-white h2">Restricted area access</p>
                <p class="white mb-0">
                  Please use this form to login.
                  <br>To create new account please
                  <NuxtLink to="/signup" class="white btn-link">signup</NuxtLink>
                  or go back
                  <NuxtLink to="/" class="white btn-link">home</NuxtLink>
                </p>
              </div>
              <div class="form-side">
                <h6 class="mb-4">Login</h6>
                <client-only>
                  <LoginForm/>
                </client-only>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import LoginForm from "~/components/auth/LoginForm.vue";
import Component from "vue-class-component";

@Component({
  components: {
    LoginForm
  },
  head: { bodyAttrs: {class: "rounded background"}}
})
export default class LoginPage extends Vue {
}

</script>
