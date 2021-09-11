<template>
    <div class="disable-text-selection">
      <b-row class="app-row survey-app">
        <Colxx xxs="12">
          <div class="mb-2">
            <h1>{{ $t('todo.todo-list') }}</h1>
            <div class="top-right-button-container">
              <b-button
                v-b-modal.modalright
                variant="primary"
                size="lg"
                class="top-right-button"
              >{{ $t('todo.add-new') }}
              </b-button>
              <b-button-group>
                <b-dropdown
                  split
                  right
                  @click="todoStore.selectAll(true)"
                  class="check-button"
                  :disabled="todoStore.hasAnyItemVisible"
                  variant="primary"
                >
                  <label
                    class="custom-control custom-checkbox pl-4 mb-0 d-inline-block"
                    slot="button-content"
                  >
                    <input
                      class="custom-control-input"
                      type="checkbox"
                      :checked="todoStore.isSelectedAll"
                    />
                    <span
                      :class="{
                      'custom-control-label' :true,
                      'indeterminate' : todoStore.isAnyItemSelected
                    }"
                    >&nbsp;</span>
                  </label>
                  <b-dropdown-item @click="todoStore.onStatusChange(true)">{{ $t('todo.action-completed') }}</b-dropdown-item>
                  <b-dropdown-item @click="todoStore.onStatusChange(false)">{{ $t('todo.action-pending') }}</b-dropdown-item>
                </b-dropdown>
              </b-button-group>
            </div>
            <todo-add-new-modal :categories="todoStore.categoriesNewItem"
                                :labels="todoStore.labelsNewItem"
                                :statuses="todoStore.statuses"></todo-add-new-modal>

          </div>
          <div class="separator mb-5"/>

          <b-row key="itemList">
            <Colxx xxs="12" v-for="(item,index) in todoStore.items" :key="`item${index}`">
              <todo-list-item
                :key="item.id"
                :item="item"
                @toggle-item="todoStore.toggleItem"
              />
              <!-- v-contextmenu:contextmenu -->
            </Colxx>
          </b-row>
        </Colxx>
      </b-row>

      <todo-application-menu :items="todoStore.items"
                             :categories="todoStore.categories"
                             :labels="todoStore.labels"></todo-application-menu>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import TodoListItem from "~/components/app/todo/TodoListItem.vue"
import {TodoStore} from "~/store/modules/app/todo-store";
import Colxx from "~/components/common/Colxx.vue";
import Breadcrumb from "~/components/common/Breadcrumb.vue";
import {proxy} from "~/store/store";
import TodoApplicationMenu from '~/components/app/todo/TodoApplicationMenu.vue'
import TodoAddNewModal from '~/components/app/todo/TodoAddNewModal.vue';

@Component({
  components: {
    TodoListItem,
    Colxx,
    Breadcrumb,
    TodoApplicationMenu,
    TodoAddNewModal
  },
  head: {bodyAttrs: {class: "rounded"}}
})
export default class TodoMain extends Vue {

  todoStore: TodoStore = proxy.todoStore

  mounted() {
    this.todoStore.onMounted()
  }

}
</script>

