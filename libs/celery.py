"""
Management command for managing celery

Alternate Command: celery -A factory.celery worker --loglevel=info
"""

import logging
from copy import deepcopy
from flask_script import Command
from celery import current_app as celery_app
from celery.bin import worker
from flask_script import Option
from factory import celery

from settings.settings_celery import CELERY_WORKER_CONFIG
from settings import APP_ENV

logger = logging.getLogger(__name__)


class CeleryWorker(Command):
    """Starts the celery worker."""
    name = 'celery'
    capture_all_args = True

    option_list = (
        Option('--queues', '-Q', dest='queues'),
        Option('--logfile', '-L', dest='logfile')
    )

    def run(self, argv, queues=None, logfile=None):
        config = deepcopy(CELERY_WORKER_CONFIG)
        if logfile:
            config.update(logfile=logfile)
        if queues:
            config.update(queues=queues.split(','))
            logger.info("worker is listening to queues: {}".format(queues))
        else:
            logger.info("worker is listening to ALL queues")

        application = celery_app._get_current_object()
        w = worker.worker(app=application)
        logger.debug("celery environment : {}".format(APP_ENV))
        w.run(**config)
