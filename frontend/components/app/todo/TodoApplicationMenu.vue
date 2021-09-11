<template>
  <application-menu>
    <perfect-scrollbar :settings="{ suppressScrollX: true, wheelPropagation: false }">
      <div class="p-4">
        <p class="text-muted text-small mb-3">{{$t('todo.status')}}</p>
        <ul class="list-unstyled mb-4">
          <li class="nav-item">
            <a href="#" @click.prevent.stop="filterByStatusAll()">
              <b-icon icon="check-all" font-scale="2.0" variant="info" class="p-1"/>
              <span class="d-inline-block" >{{$t('todo.all-tasks')}}</span>
              <span class="float-right">{{items.length}}</span>
            </a>
          </li>
          <li class="nav-item">
            <a href="#" @click.prevent.stop="filterByStatusPending()">
              <b-icon icon="hand-thumbs-down" font-scale="2.0" variant="danger" class="p-1"/>
              <span class="d-inline-block" >{{$t('todo.pending-tasks')}}</span>
              <span class="float-right">{{countPending()}}</span>
            </a>
          </li>
          <li class="nav-item">
            <a href="#" @click.prevent.stop="filterByStatusCompleted()">
              <b-icon icon="hand-thumbs-up" font-scale="2.0" variant="primary" class="p-1"/>
              <span class="d-inline-block">{{$t('todo.completed-tasks')}}</span>
              <span class="float-right">{{countCompleted()}}</span>
            </a>
          </li>
        </ul>
        <p class="text-muted text-small mb-1">{{$t('todo.categories')}}</p>
        <ul class="list-unstyled mb-4">
          <b-form-radio-group
            stacked
            class="pt-2"
            @change="onCategorySelect"
            :options="this.categories.map((c)=> { return {text:c, value:c}})"
          />
        </ul>
        <p class="text-muted text-small mb-3">{{$t('todo.labels')}}</p>
        <div>
          <p class="d-sm-inline-block mb-1" v-for="(l,index) in labels" :key="index">
            <a href="#" @click.prevent.stop="onBadgeClick(l)">
              <b-badge pill
                       :variant="`outline-${color(l)}`"
                       class="mb-1 mr-1">{{l}}</b-badge>
            </a>
          </p>
        </div>
      </div>
    </perfect-scrollbar>
  </application-menu>
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import ApplicationMenu from "~/components/common/ApplicationMenu.vue";
import {
  TODO_LABEL_TO_COLOR,
  TodoStatus,
  TodoStore,
  UIFetchStatus, UIFilterOption
} from "~/store/modules/app/todo-store"
import {proxy} from "~/store/store";

const TodoApplicationMenuProps = Vue.extend({
  props: {
    categories: Array,
    labels: Array,
    items: Array
  }
})

@Component({
  components: {
    ApplicationMenu
  }
})
export default class TodoApplicationMenu extends TodoApplicationMenuProps {

  todoStore: TodoStore = proxy.todoStore

  mounted() {
    document.body.classList.add("right-menu")
  }

  beforeDestroy() {
    document.body.classList.remove("right-menu")
  }

  countPending() {
    return this.items.filter((item: any) => item.status === TodoStatus.PENDING).length
  }

  countCompleted() {
    return this.items.filter((item: any) => item.status === TodoStatus.COMPLETED).length
  }

  color(filterOption: UIFilterOption){
    return TODO_LABEL_TO_COLOR[filterOption]
  }

  async filterByStatusAll(){
    await this.todoStore.fetchAllItems(UIFetchStatus.ALL, false)
  }

  async filterByStatusPending(){
    await this.todoStore.fetchAllItems(UIFetchStatus.PENDING, false)
  }

  async filterByStatusCompleted(){
    await this.todoStore.fetchAllItems(UIFetchStatus.COMPLETED, false)
  }

  async onBadgeClick(selectedLabel: UIFilterOption) {
    this.todoStore.filterByLabel(selectedLabel)
  }

  async onCategorySelect(selectedCategory: string) {
    this.todoStore.filterByCategory(selectedCategory)
  }

}
</script>

