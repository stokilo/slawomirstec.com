from chalicelib.dao.contact import ContactEntity
from chalicelib.dao.monitoring.email_monitoring import EmailMonitoringDao
from chalicelib.model.constants import AWSConstants
from chalicelib import logger
import boto3


def on_table_update_handler(event):
    """Handler for dynamodb stream with contacts records, we listen on events
    when new contact is created and send email to admin.

    There is a limit of email that we can send to avoid flooding admin mailbox
    """
    for record in event:
        try:
            pk = record.new_image["pk"]["S"]
            if str.startswith(pk, ContactEntity().prefix()):
                name = record.new_image["name"]["S"]
                email = record.new_image["email"]["S"]
                details = record.new_image["details"]["S"]
                subject = "PyAws contact created"
                message = f"Email from: {name} {email} message: {details}"
                send_email_to_admin(subject, message, 100)

        except Exception as e:
             logger.exception(e)


def send_email_to_admin(subject: str, message: str, max_emails_allowed_to_be_sent: int = 100):
    """Send email to admin account
    """
    try:
        email_config = EmailMonitoringDao().load()
        if email_config.max_emails_allowed_to_be_sent > max_emails_allowed_to_be_sent:
            logger.info(f"max_emails_allowed_to_be_sent reached {max_emails_allowed_to_be_sent}")
            return

        client = boto3.client('ses',
                              region_name=AWSConstants.SNS_EMAIL_REGION.value)
        response = client.send_email(
            Destination={
                'ToAddresses': [AWSConstants.SNS_EMAIL_VERIFIED_SENDER.value]
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': message
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject
                },
            },
            Source=AWSConstants.SNS_EMAIL_VERIFIED_SENDER.value,
        )
        email_config.email_send()
        dir(response)
    except Exception as e:
       logger.exception(e)


