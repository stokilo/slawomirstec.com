from chalicelib.dao.dashboard import DashboardDao
from chalicelib.dao.migration.shared import BaseMigration
from chalicelib.dao.monitoring.email_monitoring import EmailMonitoringDao
from chalicelib.dao.monitoring.lambda_invocation_monitoring import LambdaInvocationMonitoringDao


class Migration_0_1_0(BaseMigration):
    """Initial migration for PyAws
    """

    def __init__(self):
        super().__init__("0.1.0")

    def migrate(self):
        super().log("Create email monitoring")
        email_monitoring_dao = EmailMonitoringDao()
        email_monitoring = email_monitoring_dao.load()
        email_monitoring.save()

        super().log("Create lambda monitoring")
        lambda_dao = LambdaInvocationMonitoringDao()
        lambda_monitoring = lambda_dao.load()
        lambda_monitoring.save()

        super().log("Create dashboard")
        dashboard_dao = DashboardDao()
        dashboard = dashboard_dao.load()
        dashboard.save()
        pass