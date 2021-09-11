from datetime import datetime
from typing import List

import ksuid
from pynamodb.models import Model

from pynamodb.attributes import UTCDateTimeAttribute, NumberAttribute, UnicodeAttribute

from chalicelib.dao.strategies.strategy_base import BaseSingletonEntityForPyAwsV1, BaseEntityForPyAwsV1, BaseDao
from chalicelib.model.dashboard import DashboardLogItemType


class DashboardStats(BaseSingletonEntityForPyAwsV1):
    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    contactCount = NumberAttribute(default=0, null=False)
    userCount = NumberAttribute(default=0, null=False)
    todoCount = NumberAttribute(default=0, null=False)
    last_change_date = UTCDateTimeAttribute()

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.last_change_date = datetime.utcnow()

    def prefix(self) -> str:
        return "DASHBOARD#DASHBOARD_STATS#"


class DashboardAuditLogItemEntity(BaseEntityForPyAwsV1):
    """Entity for dashboard audit log items
    """
    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    def __init__(self, unique_id: str = "", **kwarg):
        super().__init__(unique_id, **kwarg)
        # Shared pk with DashboardStats entity, different sort key, we want to fetch them both in single call
        self.pk = self.get_pk("")
        self.sk = self.get_sk(unique_id)
        self.gsi1pk = self.get_pk("")
        self.gsi1sk = self.get_sk(unique_id)

    type = UnicodeAttribute(null=False)
    creation_date = UTCDateTimeAttribute(null=False)

    def get_sk(self, unique_id: str):
        # ## because of sort order
        return f"#{self.prefix()}{unique_id}"

    def prefix(self) -> str:
        return "DASHBOARD#DASHBOARD_STATS#"


class DashboardStatsAndLogsView(Model):
    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    gsi1pk = UnicodeAttribute()
    gsi1sk = UnicodeAttribute()
    contactCount = NumberAttribute(default=0, null=False)
    userCount = NumberAttribute(default=0, null=False)
    todoCount = NumberAttribute(default=0, null=False)
    last_change_date = UTCDateTimeAttribute()
    type = UnicodeAttribute(null=False)
    creation_date = UTCDateTimeAttribute(null=False)

    def prefix(self) -> str:
        return "DASHBOARD#DASHBOARD_STATS#"


class DashboardDao(BaseDao[DashboardStats]):

    @staticmethod
    def load() -> DashboardStats:
        dashboard_stats: DashboardStats = DashboardStats()
        return BaseDao.get(dashboard_stats, dashboard_stats.get_pk(""), dashboard_stats.get_sk(""))

    @staticmethod
    def update_dashboard(transaction,
                         update_contact: bool = False,
                         update_user: bool = False,
                         update_todo: bool = False):
        """Common function for all tracked entities to increase count of items we show on the dashboard
        """

        dashboard_stats = DashboardStats()
        actions = [DashboardStats.last_change_date.set(datetime.now())]

        if update_contact:
            actions.append(DashboardStats.contactCount.set(DashboardStats.contactCount + 1))
        if update_user:
            actions.append(DashboardStats.userCount.set(DashboardStats.userCount + 1))
        if update_todo:
            actions.append(DashboardStats.todoCount.set(DashboardStats.todoCount + 1))

        transaction.update(
            dashboard_stats,
            actions=actions
        )

    @staticmethod
    def add_audit_event(transaction, item_type: DashboardLogItemType):
        audit_event = DashboardAuditLogItemEntity(ksuid.ksuid().__str__())
        audit_event.type = item_type.value
        audit_event.creation_date = datetime.utcnow()
        transaction.save(audit_event)

    def get_dashboard(self) -> List[DashboardStatsAndLogsView]:
        items = []
        dashboard_view = DashboardStatsAndLogsView()
        dashboard_view.pk = dashboard_view.prefix()
        item_iterator = DashboardStatsAndLogsView.query(dashboard_view.pk, limit=10, scan_index_forward=False)
        for item in item_iterator:
            items.append(item)
        return items