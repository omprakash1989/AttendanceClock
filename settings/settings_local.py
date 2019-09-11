"""
Settings sample file.
"""
import enum

DEBUG = False
SQLALCHEMY_DATABASE_URI = "postgres://wxitcnhdxahlvi:4b84e2f830999ee136366f4e7302d3f9eb1c7a3ca5b73c42ac1cc9043f7607ed@ec2-174-129-229-106.compute-1.amazonaws.com:5432/d22tess123bs21"
TESTING = True

# API rate limit count.
LIMITER = 0

# This is the s3 bucket creds for punching_clock report/CIR files upload.
AWS_BUCKET = ""
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""

# Sentry DSN if sentry is added.
SENTRY_DSN = ''

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application base url.
TEST_BASE_URL = 'http://127.0.0.1:5000'

# Test sqlalchemy config for test database.
# This is non persistent and teared down after test completed.
TEST_SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost/lss_test"

# punching_clock report expiry threshold in days.
REFRESH_DAYS = 40

# This hold the creds of different punching_clock service API creds and timeout also.
ATTENDANCECLOCK_SERVICE_DETAILS = {
    "CIBIL": {
        "host": "",
        "port": "",
        "timeout": 5,
    }
}

# Environment.
ENV = 'local'

# This is the Basic auth creds for credit line API.
CREDIT_LINE_API_AUTH = {
    "username": "Bearer",
    "password": "1234"
}

CIBIL_REPORT_API_AUTH = {
    "username": "lss_attendance_clock_viewer",
    "password": "4Z4UKK"
}

ERROR_MAIL_RECEIVERS = []
ATTENDANCECLOCK_RESPONSE_ERROR_MAIL_RECEIVERS = []
ERROR_MAIL_SENDER = ''

# SES credentials used for mailing service.
AWS_SES_ACCESS_KEY = ""
AWS_SES_SECRET_KEY = ""

AWS_SES_REGION_NAME = ''
AWS_SES_REGION_ENDPOINT = ''
AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'

CELERY_BROKER_URL = 'amqp://'
# Slack API token.
SLACK_TOKEN = ''


class ProxyServerEnum(enum.Enum):
    ACTIVE = False
    HOST = ""
    PORT = 0

# Redis host and port.
REDIS_HOST = '127.0.0.1'
REDIS_PORT = int('6379')

