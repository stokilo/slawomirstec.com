import {SERVER_API_ROUTES} from "~/store/api/routes";
import AxiosService from "~/store/api/axios-service";
import {Status} from "~/store/model/shared";
import {UIFetchStatus} from "~/store/modules/app/todo-store";
import {Dashboard, DashboardGetResult, DashboardStats} from "~/store/model/app/dashboard";

export default class DashboardService extends AxiosService {

  async getDashboard(status: UIFetchStatus = UIFetchStatus.ALL): Promise<DashboardGetResult> {
    return super.genericFetch(SERVER_API_ROUTES.ROUTE_DASHBOARD,
      new DashboardGetResult(new Dashboard(new DashboardStats(0, 0,0), []), new Status()),
      {status: status})
  }
}
