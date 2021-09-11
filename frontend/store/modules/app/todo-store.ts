import {action, createModule, mutation} from "vuex-class-component";
import TodoService from "~/store/api/app/todo-service";
import {Todo, TodosArray} from "~/store/model/app/todo";
import {$notify, $i18n, $loader} from "~/utils/api";

export const VuexModule = createModule({
  namespaced: "todo-store",
  strict: false,
  target: "nuxt"
});

export enum LabelColor {
  INFO = "info",
  PRIMARY = "primary",
  SECONDARY = "secondary"
}

export const TODO_LABEL_TO_COLOR: Record<UIFilterOption, LabelColor> = {
  ALL: LabelColor.PRIMARY,
  EDUCATION: LabelColor.PRIMARY,
  NEW_FRAMEWORK: LabelColor.SECONDARY,
  PERSONAL: LabelColor.INFO
}

export enum TodoStatus {
  PENDING = "PENDING",
  COMPLETED = "COMPLETED"
}

export enum TodoLabel {
  EDUCATION = "EDUCATION",
  NEW_FRAMEWORK = "NEW_FRAMEWORK",
  PERSONAL = "PERSONAL"
}

export enum TodoCategory {
  JAVA = "JAVA",
  PYTHON = "PYTHON",
  SASS = "SASS"
}

export enum UIFetchStatus {
  ALL = "",
  PENDING = "PENDING",
  COMPLETED = "COMPLETED"
}

export enum UIFilterCategory {
  ALL = "ALL",
  JAVA = "JAVA",
  PYTHON = "PYTHON",
  SCALA = "SCALA"
}

export enum UIFilterOption {
  ALL = "ALL",
  EDUCATION = "EDUCATION",
  NEW_FRAMEWORK = "NEW_FRAMEWORK",
  PERSONAL = "PERSONAL"
}

export class TodoStore extends VuexModule {

  todoService: TodoService = new TodoService()

  categories: Array<UIFilterCategory> = [UIFilterCategory.ALL, UIFilterCategory.JAVA, UIFilterCategory.PYTHON, UIFilterCategory.SCALA]
  categoriesNewItem: Array<UIFilterCategory> = this.categories.filter((category) => category != UIFilterCategory.ALL)

  labels: Array<UIFilterOption> = [UIFilterOption.ALL, UIFilterOption.EDUCATION, UIFilterOption.NEW_FRAMEWORK, UIFilterOption.PERSONAL]
  labelsNewItem: Array<UIFilterOption> = this.labels.filter((label) => label != UIFilterOption.ALL)

  statuses: Array<TodoStatus> = [TodoStatus.PENDING, TodoStatus.COMPLETED]

  items: Array<Todo> = []
  isSelectedAll: boolean = false

  @mutation
  addItem(todo: Todo) {
    this.items.push(todo)
  }

  @mutation
  addItems(todoItems: Array<Todo>) {
    this.items = []
    todoItems.forEach((item, index) => {

      const status: TodoStatus = TodoStatus[item.status as keyof typeof TodoStatus]
      const label: TodoLabel = TodoLabel[item.label as keyof typeof TodoLabel]
      const category: TodoCategory = TodoCategory[item.category as keyof typeof TodoCategory]

      this.items.push(new Todo(item.id, item.date, item.subject, item.details, status, category, label))
    })
  }

  @mutation
  filterByCategory(selectedCategory: string) {
    this.items.map((item) => item.isVisible = item.category == selectedCategory || selectedCategory == UIFilterCategory.ALL)
  }

  @mutation
  filterByLabel(selectedLabel: string) {
    this.items.map((item) => item.isVisible = item.label == selectedLabel || selectedLabel == UIFilterOption.ALL)
  }

  @mutation
  clearItems() {
    this.items = []
  }

  @mutation
  selectAll() {
    this.items.map(item => item.isSelected = !this.isSelectedAll)
    this.isSelectedAll = !this.isSelectedAll
  }

  @mutation
  uncheckAll() {
    this.items.map((item) => item.isSelected = false)
    this.isSelectedAll = false
  }

  @mutation
  changeSelection(itemId: string) {
    this.items.filter(item => item.id === itemId).map(item => item.isSelected = !item.isSelected)
  }

  @action
  async onMounted() {
    await this.fetchAllItems(UIFetchStatus.ALL, true)
  }

  @action
  async fetchAllItems(fetchStatus: UIFetchStatus, isInitialLoad: boolean = false) {
    let loader = $loader.show()
    try {
      this.clearItems()
      let todoGetResult = UIFetchStatus.ALL ? await this.todoService.getTodo() :
        await this.todoService.getTodo(fetchStatus)
      this.addItems(todoGetResult.items)
    } catch (error) {
      $notify("error", $i18n.t("todo.action-load-msg-title"), $i18n.t("todo.action-load-msg-error"));
    }

    if (!isInitialLoad) {
      $notify("success", $i18n.t("todo.action-load-msg-title"), $i18n.t("todo.action-load-msg-success"));
    }

    setTimeout(() => {
      loader.hide()
    }, 900)
  }

  @action
  async toggleItem(itemId: string) {
    this.changeSelection(itemId)
  }

  @action
  async refreshTodo() {
    await this.onMounted()
  }

  @action
  async onStatusChange(isCompleted: boolean) {
    const expectedStatus = isCompleted ? TodoStatus.PENDING : TodoStatus.COMPLETED
    const newStatus = isCompleted ? TodoStatus.COMPLETED : TodoStatus.PENDING
    const checkedItems = this.items.filter((item) => item.isSelected && item.status == expectedStatus)
      .map((item) => {
        item.status = newStatus
        return item
      })

    if (!checkedItems.length) {
      $notify("error", $i18n.t("todo.action-msg-title"), $i18n.t("todo.action-msg-none-selected"));
      return
    }

    let loader = $loader.show()
    let result = await this.todoService.completeTodos(new TodosArray(checkedItems))

    setTimeout(() => {
      loader.hide()
    }, 900)

    if (result.status.success) {
      $notify("success", $i18n.t("todo.action-msg-title"), $i18n.t("todo.action-msg-success"));
    } else {
      $notify("error", $i18n.t("todo.action-msg-title"), $i18n.t("todo.action-msg-error"));
    }
    this.uncheckAll()
  }

  get hasAnyItemVisible(): boolean {
    return !this.items.filter(item => item.isVisible).length
  }

}

