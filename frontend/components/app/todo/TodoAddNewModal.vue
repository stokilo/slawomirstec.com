<template>
  <b-modal
    id="modalright"
    ref="modalright"
    :title="$t('todo.add-new-title')"
    modal-class="modal-right"
  >
    <b-form>
      <div role="alert" class="alert alert-danger" :hidden="errorMessage.length <= 0">
        {{ errorMessage }}
      </div>
      <b-form-group :label="$t('todo.title')">
        <b-form-input v-model="newItem.subject" maxlength="249"/>
      </b-form-group>
      <b-form-group :label="$t('todo.detail')">
        <b-form-textarea v-model="newItem.details" :rows="2" :max-rows="2" maxlength="249"/>
      </b-form-group>
      <b-form-group :label="$t('todo.category')">
        <v-select :options="categories" v-model="newItem.category" :reduce="category => category" maxlength="249"/>
      </b-form-group>
      <b-form-group :label="$t('todo.label')">
        <v-select :options="labels" v-model="newItem.label" :reduce="label => label" maxlength="249"/>
      </b-form-group>
    </b-form>
    <template slot="modal-footer">
      <b-button variant="outline-secondary" @click="hideModal('modalright')">{{ $t('todo.cancel') }}</b-button>
      <b-button variant="primary" @click="addItem()" :disabled="!isSubmitEnabled" class="mr-1">{{
          $t('todo.submit')
        }}
      </b-button>
    </template>
  </b-modal>
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import ApplicationMenu from "~/components/common/ApplicationMenu.vue";
import {TodoStatus, TodoStore} from "~/store/modules/app/todo-store";
import TodoService from "~/store/api/app/todo-service";
import {proxy} from "~/store/store";
import {$i18n} from "~/utils/api";
import {Todo} from "~/store/model/app/todo";

@Component({
  components: {
    ApplicationMenu
  },
  props: {
    categories: Array,
    labels: Array,
    statuses: Array
  }
})
export default class TodoAddNewModal extends Vue {

  newItem: Todo = new Todo()
  errorMessage: string = ""

  todoService: TodoService = new TodoService()
  todoStore: TodoStore = proxy.todoStore

  isSubmitEnabled: boolean = true

  async addItem() {
    this.isSubmitEnabled = false
    try {
      this.newItem.status = TodoStatus.PENDING
      let newTodoResult = await this.todoService.saveTodo(this.newItem)
      if (newTodoResult.status.success) {
        await this.todoStore.refreshTodo()
        await this.hideModal("modalright")
      } else {
        this.errorMessage = $i18n.t("todo.error")
      }
    } catch (error) {
      this.errorMessage = $i18n.t("todo.error")
    }

    this.isSubmitEnabled = true
    this.newItem = new Todo()
  }

  hideModal(refName: string) {
    //@ts-ignore
    this.$refs[refName].hide();
  }

}
</script>

