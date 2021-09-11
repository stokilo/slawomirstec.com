/**
 * Model for todo_item
 */
import {Status, WithFromJson} from "~/store/model/shared"
import {TODO_LABEL_TO_COLOR, UIFilterOption} from "~/store/modules/app/todo-store";

export class TodoModelSubmitResult extends WithFromJson{
   public todoModel: Todo
   public status: Status

  constructor(todoModel: Todo, status: Status) {
    super();
    this.todoModel = todoModel;
    this.status = status;
  }
}

export class TodoGetResult extends WithFromJson{
  public items: Array<Todo> = []
  public status: Status

  constructor(items: Array<Todo>, status: Status) {
    super();
    this.items = items;
    this.status = status;
  }
}

export class Todo extends WithFromJson{
  public id: string
  public date: string
  public subject : string
  public details : string
  public status : string
  public category : string
  public label: string

  public isSelected: boolean = false
  public isVisible: boolean = true

  constructor(id: string = "", date: string = "", subject: string = "",
              details: string = "", status: string = "", category: string = "", label: string = "") {
    super();
    this.id = id;
    this.date = date;
    this.subject = subject;
    this.details = details;
    this.status = status;
    this.category = category;
    this.label = label;
  }

  color() {
    const label: UIFilterOption = UIFilterOption[this.label as keyof typeof UIFilterOption]
    return TODO_LABEL_TO_COLOR[label]
  }

}

export class TodosArray extends WithFromJson {
  public todos: Array<Todo> = []

  constructor(todos: Array<Todo>) {
    super();
    this.todos = todos;
  }
}

