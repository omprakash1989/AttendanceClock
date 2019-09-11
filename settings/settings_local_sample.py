"""
Settings sample file.
"""
import enum

DEBUG = True
SQLALCHEMY_DATABASE_URI = ""
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

# Redis host and port.
REDIS_HOST = ''
REDIS_PORT = ''
