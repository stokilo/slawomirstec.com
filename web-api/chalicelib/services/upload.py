import uuid

import boto3
from chalicelib import logger
from chalicelib.model.constants import AWSConstants
from chalicelib.model.shared import Status
from chalicelib.model.upload import SignedUploadUrlResponse
import datetime


class UploadService:

    def __init__(self) -> None:
        pass

    def created_signed_url_profile_update(self):
        now = datetime.datetime.now()
        object_name = f"{now.year}/{now.month}/{now.day}/{now.hour}/profile_image_{uuid.uuid4()}.png"
        return self.create_signed_url_for_post_upload(object_name)

    @staticmethod
    def create_signed_url_for_post_upload(s3_object_name: str) -> SignedUploadUrlResponse:
        """Generate a signed URL S3 POST request to upload a file
        """
        upload_signed_url = SignedUploadUrlResponse({}, Status())
        try:
            s3_client = boto3.client('s3')
            bucket_name = f"{AWSConstants.PYAWS_CLI_IMAGE_SUBDOMAIN.value}.{AWSConstants.SSM_PARAMETER_PYAWS_CLI_DOMAIN.value}"
            conditions = [
                ["content-length-range", 0, 1048576]
            ]

            upload_response = s3_client.generate_presigned_post(bucket_name,
                                                                s3_object_name,
                                                                Fields=None,
                                                                Conditions=conditions,
                                                                ExpiresIn=60)
            upload_signed_url.upload = upload_response
            upload_signed_url.status.success = True
        except Exception as e:
            logger.exception(e)
            upload_signed_url.status.success = False
        return upload_signed_url


uploadService = UploadService()
