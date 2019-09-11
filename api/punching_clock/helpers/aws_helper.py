"""
AWSHelper Class

This class will handle the aws/s3 related tasks.

Exceptions in this class is not suppressed.
"""

import os
import logging

from settings import s3_client
from api.constants import AWS_S3_URL_PATTERN

logger = logging.getLogger("punching_clock")


class AWSHelper:

    def __init__(self, bucket):
        """
        Constructor.

        :param bucket: String
        s3 bucket name on which the operation is to be performed.
        """

        self.bucket = bucket

    def upload(self, file_key, file, remove_original_file=True):
        """
        Upload file to s3.

        :param file_key: String
        key of the file.

        :param file: String
        File path.

        :param remove_original_file: Boolean
        True if local file to be deleted else False.

        :return: s3_url String
        The accessible url of uploaded file.
        """

        s3_url = ""
        try:
            s3_client.upload_file(file, self.bucket, file_key)
            s3_url = AWS_S3_URL_PATTERN.format(self.bucket, file_key)

        except Exception as exc:
            logging.exception("Exception: {} occurred while uploading the file: {} to bucket: {}.".format(exc, file_key,
                                                                                                          self.bucket))

        # Remove local file.
        if remove_original_file:
            try:
                os.remove(file)
            except OSError:
                pass

        return s3_url

    def download(self, file_key, file):
        """
        Download the file from s3 and save as file.

        :param file_key: String
        S3 file key to be downloaded.

        :param file:
        File path to save the downloaded file.

        :return: String
        Downloaded file path.
        """

        try:
            # Download the file.
            s3_client.download_file(self.bucket, file_key, file)

        except Exception as exc:
            logging.exception("Exception: {} occurred while downloading the file: {} to bucket: {}.".format(
                exc, file_key, self.bucket))
        return file
