import {SERVER_API_ROUTES} from "~/store/api/routes";
import AxiosService from "~/store/api/axios-service";
import {Status} from "~/store/model/shared";
import {Todo, TodoGetResult, TodoModelSubmitResult, TodosArray} from "~/store/model/app/todo";
import {UIFetchStatus} from "~/store/modules/app/todo-store";

export default class TodoService extends AxiosService {

  async saveTodo(todo: Todo): Promise<TodoModelSubmitResult> {
    return super.genericPost(SERVER_API_ROUTES.ROUTE_TODO, todo, new TodoModelSubmitResult(
      new Todo(), new Status())
    )
  }

  async getTodo(status: UIFetchStatus = UIFetchStatus.ALL): Promise<TodoGetResult> {
    return super.genericFetch(SERVER_API_ROUTES.ROUTE_TODO,
      new TodoGetResult([], new Status()),
      {status: status})
  }

  async completeTodos(todos: TodosArray): Promise<TodoModelSubmitResult> {
    return super.genericPost(SERVER_API_ROUTES.ROUTE_TODO_BATCH, todos, new TodoModelSubmitResult(new Todo(), new Status()))
  }

}
