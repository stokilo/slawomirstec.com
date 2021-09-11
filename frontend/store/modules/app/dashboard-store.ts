import {action, createModule, mutation} from "vuex-class-component";
import DashboardService from "~/store/api/app/dashboard-service";
import {Dashboard, DashboardGetResult, DashboardStats} from "~/store/model/app/dashboard";
import {$i18n, $loader, $notify} from "~/utils/api";

export const VuexModule = createModule({
  namespaced: "dashboard-store",
  strict: false,
  target: "nuxt"
});
export class DashboardStore extends VuexModule {

  dashboardService: DashboardService = new DashboardService()

  dashboard: Dashboard = new Dashboard(new DashboardStats(0, 0,0), [])

  @mutation
  dashboardUpdate(newDashboard: Dashboard) {
    let stats = newDashboard.stats
    this.dashboard.stats = new DashboardStats(stats.contactCount, stats.userCount, stats.todoCount)
    this.dashboard.logs = newDashboard.logs
  }

  @action
  async onMounted() {
    let loader = $loader.show()
    try {
      let result: DashboardGetResult = await this.dashboardService.getDashboard()
      if (result.status.success) {
        this.dashboardUpdate(result.dashboard)
      }
    }catch(error){
      $notify("error", $i18n.t("dashboard.action-load-msg-title"), $i18n.t("dashboard.action-load-msg-error"));
    }
    setTimeout(() => {
      loader.hide()
    }, 900)
  }

}

