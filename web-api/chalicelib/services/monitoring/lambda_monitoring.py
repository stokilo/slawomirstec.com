from chalicelib.dao.monitoring.lambda_invocation_monitoring import LambdaInvocationMonitoringDao
from datetime import datetime, timezone, timedelta
from chalicelib import logger
import boto3
import os


def lambda_invocation_count_monitoring(number_of_invocations_to_trigger_sms: int = 3000,
                                       number_of_seconds_before_next_sms_is_allowed: int = 3600,
                                       max_sms_allowed_to_be_send: int = 30,
                                       sms_nr: str = ""):

    """Trigger sms notification when we detect high number of lambdas execution.
    It monitors metric: sum of all lambda functions invocations in last hour
    """
    try:

        client = boto3.client('cloudwatch', region_name=os.environ['AWS_DEFAULT_REGION'])
        response = client.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName="Invocations",
            StartTime=datetime.utcnow() - timedelta(minutes=60),
            EndTime=datetime.utcnow(),
            Period=3600,
            Statistics=[
                "Sum",
            ]
        )
        data_points_array = response["Datapoints"]
        sum_lambda_invocations_last_hour = 0
        if len(data_points_array) > 0:
            sum_lambda_invocations_last_hour = int(data_points_array[0]["Sum"])
        logger.info(f"sum_lambda_invocations_last_hour {sum_lambda_invocations_last_hour} "
              f"number_of_invocations_to_trigger_sms {number_of_invocations_to_trigger_sms}")

        if sum_lambda_invocations_last_hour > number_of_invocations_to_trigger_sms:
            lambda_invocation_dao = LambdaInvocationMonitoringDao()
            lambda_invocation_monitoring = lambda_invocation_dao.load()

            if lambda_invocation_monitoring.max_sms_allowed_to_be_send > max_sms_allowed_to_be_send:
                logger.info(f"triggered anti sms flood protection, {max_sms_allowed_to_be_send}")
                return

            now = datetime.now(timezone.utc)
            nr_of_second_since_last_sms = int((now - lambda_invocation_monitoring.last_sms_sent_time).total_seconds())

            logger.info(f"nr_of_second_since_last_sms {nr_of_second_since_last_sms}"
                         f" number_of_seconds_before_next_sms_is_allowed {number_of_seconds_before_next_sms_is_allowed}")
            if nr_of_second_since_last_sms == 0 or \
               nr_of_second_since_last_sms > number_of_seconds_before_next_sms_is_allowed:
                lambda_invocation_monitoring.lambda_invocation_count_last_hour = sum_lambda_invocations_last_hour
                lambda_invocation_monitoring.last_sms_sent_time = now
                lambda_invocation_monitoring.max_sms_allowed_to_be_send = \
                    lambda_invocation_monitoring.max_sms_allowed_to_be_send + 1
                lambda_invocation_monitoring.save()

                logger.info(f"Sending notification to admin, number of lambda invocations {sum_lambda_invocations_last_hour}")
                sns = boto3.client('sns')
                sns.publish(PhoneNumber=sms_nr, Message=f"Check number of lambda invocation in last hour"
                                                        f" {sum_lambda_invocations_last_hour}")
            else:
                logger.info(f"Number of seconds from last sms {nr_of_second_since_last_sms}, don't send sms")
        else:
            logger.info(f"Lambda execution count in last hour {sum_lambda_invocations_last_hour}, no alarm")


    except Exception as e:
        logger.exception(e)
