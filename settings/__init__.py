import logging
import os
import sys

from slackclient import SlackClient
import boto3
from botocore.config import Config
import redis


APP_ENV = os.environ.get("APP_ENV", 'local')
SECRET_KEY = '8638dbfa-a27e-4382-a458-3c14364d4a5b'

logger = logging.getLogger("punching_clock")

if APP_ENV == "staging":
    from .settings_staging import *
elif APP_ENV == "production":
    from .settings_production import *
elif APP_ENV == "uat":
    from .settings_uat import *
elif APP_ENV == "docker":
    from .settings_docker import *
else:
    try:
        from .settings_local import *
    except ImportError:
        logging.error("\nOops...No local setting detected. add settings/settings_local.py with local configuration.")
        logging.error("Exiting.....\n")
        sys.exit()

# Initialize S3 connection.
# s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY,
#                          config=Config(signature_version='s3v4'))
#
# # Create a new SES resource and specify a region.
# email_client = boto3.client('ses', aws_access_key_id=AWS_SES_ACCESS_KEY, aws_secret_access_key=AWS_SES_SECRET_KEY,
#                             region_name=AWS_SES_REGION_NAME)
#
# # Slack client.
# slack_client = SlackClient(SLACK_TOKEN)
#
# # redis client.
# redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)

# Identify the timezone lookup database
GEOIP_DATA_LOCATION = "static/GeoLiteCity.dat"
CELERY_BROKER_URL = ''
