"""
Settings sample file.
"""
import enum

DEBUG = False
SQLALCHEMY_DATABASE_URI = "postgresql://omprakash:omprakash@localhost/employee_attendance"
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

# punching_clock report expiry threshold in days.
REFRESH_DAYS = 40

# Environment.
ENV = 'local'

# Redis host and port.
REDIS_HOST = '127.0.0.1'
REDIS_PORT = int('6379')

