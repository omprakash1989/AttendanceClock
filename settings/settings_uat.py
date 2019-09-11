"""
UAT settings file.
Creds and values to be retrieved from environment.
"""

import os
import enum


from api.punching_clock.helpers.misc_helper import get_bool_value

ENV = 'uat'

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
TESTING = False
LIMITER = int(os.environ.get('LIMITER', 0))
AWS_BUCKET = os.environ['AWS_BUCKET']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
SQLALCHEMY_TRACK_MODIFICATIONS = get_bool_value(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'False'))
TEST_BASE_URL = ''
TEST_SQLALCHEMY_DATABASE_URI = ''
REFRESH_DAYS = int(os.environ.get('REFRESH_DAYS', 40))


REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
