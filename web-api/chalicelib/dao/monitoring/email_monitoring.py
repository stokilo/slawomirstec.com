from datetime import datetime, timezone
from pynamodb.attributes import UTCDateTimeAttribute, NumberAttribute

from chalicelib.dao.strategies.strategy_base import BaseSingletonEntityForPyAwsV1, BaseEntityForPyAwsV1, BaseDao


class EmailMonitoring(BaseSingletonEntityForPyAwsV1):
    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    last_email_sent_date = UTCDateTimeAttribute(null=True)
    max_emails_allowed_to_be_sent = NumberAttribute(default=0)

    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def email_send(self):
        self.max_emails_allowed_to_be_sent = self.max_emails_allowed_to_be_sent + 1
        self.last_email_sent_date = datetime.now(timezone.utc)
        self.save()

    def prefix(self) -> str:
        return "INTERNAL_EMAIL_MONITORING#SINGLETON"


class EmailMonitoringDao(BaseDao[EmailMonitoring]):

    @staticmethod
    def load() -> EmailMonitoring:
        email_monitoring: EmailMonitoring = EmailMonitoring()
        return BaseDao.get(email_monitoring, email_monitoring.get_pk(""), email_monitoring.get_sk(""))

