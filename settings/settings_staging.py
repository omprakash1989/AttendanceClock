"""
Staging settings.
"""
import enum
import os

import os
import enum
ENV = 'staging'

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
TESTING = False
LIMITER = int(os.environ.get('LIMITER', 0))
AWS_BUCKET = os.environ['AWS_BUCKET']
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', '')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
SQLALCHEMY_TRACK_MODIFICATIONS = True
TEST_BASE_URL = ''
TEST_SQLALCHEMY_DATABASE_URI = ''

REDIS_HOST = 'redis'
REDIS_PORT = int('6379')

# Staging secrets are stored somewhere else and injected into the environment at the time of deployment
# If you add any new configuration please remind cluster admin to add new variables in production secrets configuration
