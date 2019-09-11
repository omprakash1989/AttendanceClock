import logging
import traceback

from flask_restplus import Api
from settings import DEBUG
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger("punching_clock")

api = Api(version='1.7.5', title='Clock Punch API',
          description='Attendance clock API.', validate=True,
          doc='/doc/')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
