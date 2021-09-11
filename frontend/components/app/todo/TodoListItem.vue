<template>
  <b-card v-if="this.item.isVisible" @click.prevent="toggleItem($event, item.id)" :class="{'d-flex mb-3':true,'active' : this.item.isSelected}" no-body>
    <div class="d-flex flex-grow-1 min-width-zero">
      <b-card-body
        class="align-self-center d-flex flex-column flex-md-row justify-content-between min-width-zero align-items-md-center pb-2">
        <a href="#" class="list-item-heading mb-0 truncate w-40 w-xs-100  mb-1 mt-1" @click.prevent="">
          <b-icon icon="hand-thumbs-down" font-scale="2.0" variant="danger" class="p-1" v-if="!isComplete(this.item)"/>
          <b-icon icon="hand-thumbs-up" font-scale="2.0" variant="primary" class="p-1" v-if="isComplete(this.item)"/>
          <span class="align-middle d-inline-block">{{ item.subject }}</span>
        </a>
        <p class="mb-1 text-muted text-small w-15 w-xs-100">{{ item.category }}</p>
        <p class="mb-1 text-muted text-small w-15 w-xs-100">{{ item.date | formatPDate }}</p>
        <div class="w-15 w-xs-100">
          <b-badge :variant="this.item.color()" pill>{{ item.label }}</b-badge>
        </div>
      </b-card-body>
      <div class="custom-control custom-checkbox pl-1 align-self-md-center align-self-start mr-4 pt-4">
        <b-form-checkbox :checked="this.item.isSelected" class="itemCheck mb-0"/>
      </div>
    </div>
    <div class="card-body pt-1"><p class="mb-0">{{this.item.details}}</p></div>
  </b-card>
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import {TodoStatus} from "~/store/modules/app/todo-store";
import {Todo} from "~/store/model/app/todo";

const TodoProps = Vue.extend({
  props: {
    item: Todo
  }
})

@Component
export default class TodoListItem extends TodoProps {

  toggleItem(event: string, itemId: string) {
    this.$emit('toggle-item', itemId)
  }

  isComplete(item: Todo): Boolean {
    return item.status == TodoStatus.COMPLETED
  }
}
</script>
