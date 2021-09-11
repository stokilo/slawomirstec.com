/**
 * Model for dashboard
 */
import {Status, WithFromJson} from "~/store/model/shared"

export class DashboardGetResult extends WithFromJson{
  public dashboard: Dashboard
  public status: Status

  constructor(dashboard: Dashboard, status: Status) {
    super();
    this.dashboard = dashboard
    this.status = status;
  }
}

export class Dashboard extends WithFromJson{
  public stats: DashboardStats = new DashboardStats()
  public logs: Array<DashboardLogItem> = []

  constructor(stats: DashboardStats, logs: Array<DashboardLogItem>) {
    super();
    this.stats = stats;
    this.logs = logs;
  }
}

export class DashboardStats extends WithFromJson{
  public contactCount: number
  public userCount: number
  public todoCount: number

  constructor(contactCount: number = 0, userCount: number = 0, todoCount: number = 0) {
    super();
    this.contactCount = contactCount;
    this.userCount = userCount;
    this.todoCount = todoCount
  }
}

export class DashboardLogItem extends WithFromJson{
  public type: string
  public label: string
  public time: string

  constructor(type: string, label: string, time: string) {
    super();
    this.type = type;
    this.label = label;
    this.time = time;
  }
}


export enum UILogItemType {
  USER_CREATION = "USER_CREATION",
  TODO_CREATION = "TODO_CREATION",
  CONTACT_CREATION = "CONTACT_CREATION"
}
