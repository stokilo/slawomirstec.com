from pynamodb.attributes import UTCDateTimeAttribute, NumberAttribute

from chalicelib.dao.strategies.strategy_base import BaseEntityForPyAwsV1, BaseSingletonEntityForPyAwsV1, BaseDao


class LambdaInvocationMonitoring(BaseSingletonEntityForPyAwsV1):
    """Metadata for lambda invocation metrics and monitoring actions
    like sms send when alarm situation is detected
    """

    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    last_sms_sent_time = UTCDateTimeAttribute(null=True)
    lambda_invocation_count_last_hour = NumberAttribute(default=0)
    max_sms_allowed_to_be_send = NumberAttribute(default=0)

    def __init__(self, **kwarg):
        super().__init__(**kwarg)

    def prefix(self) -> str:
        return "INTERNAL_LAMBDA_INVOCATION_MONITORING#SINGLETON"



class LambdaInvocationMonitoringDao(BaseDao[LambdaInvocationMonitoring]):

    @staticmethod
    def load() -> LambdaInvocationMonitoring:
        lambda_monitoring: LambdaInvocationMonitoring = LambdaInvocationMonitoring()
        return BaseDao.get(lambda_monitoring, lambda_monitoring.get_pk(""), lambda_monitoring.get_sk(""))