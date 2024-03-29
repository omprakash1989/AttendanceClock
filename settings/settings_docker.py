import os
import enum

from api.punching_clock.helpers.misc_helper import get_bool_value

ENV = 'production'

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
TESTING = False
LIMITER = int(os.environ.get('LIMITER', 0))
AWS_BUCKET = os.environ['AWS_BUCKET']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
SQLALCHEMY_TRACK_MODIFICATIONS = True
TEST_BASE_URL = ''
TEST_SQLALCHEMY_DATABASE_URI = ''
