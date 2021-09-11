<template>
  <div id="app-container" :class="menuStore.menuType">

    <Topnav/>
    <SideBar/>
    <Footer/>

    <main>
      <div class="container-fluid">
        <nuxt/>
      </div>
    </main>
  </div>
</template>


<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import SideBar from "../components/common/Sidebar.vue";
import Topnav from "../components/common/Topnav.vue";
import Footer from "../components/common/Footer.vue";
import {MenuStore} from "~/store/modules/common/menu-store";
import {proxy} from "~/store/store";

@Component({
  components: {
    Topnav,
    SideBar,
    Footer
  }
})
export default class AppLayout extends Vue {
  menuStore: MenuStore = proxy.menuStore
}

</script>
