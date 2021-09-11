from chalicelib.dao.dashboard import DashboardDao
from chalicelib.model.contact import Status
from chalicelib.model.dashboard import DashboardGetResult, Dashboard, DashboardStats, DashboardLogItem
from chalicelib import logger

class DashboardService:

    def __init__(self) -> None:
        self.dashboard_dao = DashboardDao()
        pass

    def get_dashboard(self) -> DashboardGetResult:
        result = DashboardGetResult(Dashboard(DashboardStats(0, 0, 0), []), Status())
        try:

            items = self.dashboard_dao.get_dashboard()
            for item in items:
                # First item is always main record with stats, then list of newest logs
                # Prefix fir stats is fixed and equal to sort key (sk), log items are all other
                if item.sk == item.prefix():
                    result.dashboard.stats.contactCount = item.contactCount
                    result.dashboard.stats.userCount = item.userCount
                    result.dashboard.stats.todoCount = item.todoCount
                else:
                    result.dashboard.logs.append(DashboardLogItem(item.type, item.creation_date))

            result.status.success = True

        except Exception as e:
            logger.exception(e)
            result.status.generic_error()

        return result


dashboardService = DashboardService()
