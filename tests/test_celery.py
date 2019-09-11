"""
Test cases for testing celery configurations.
"""

import unittest
from factory import initialize_app, celery

import flask

from settings.settings_celery import CELERY_BROKER_URL


class TestCelery(unittest.TestCase):
    """
    Test celery basic configuration
    """

    def get_app(self, **kwargs):
        app = initialize_app(flask.Flask('TestTask'))
        return app

    def test_broker_url_configured(self):
        # Check the broker url configuration.
        self.assertEqual(celery.conf.BROKER_URL, CELERY_BROKER_URL)

    def test_task_and_conf_check(self):
        # Creating sample task for testing.
        # With param.
        @celery.task(x=1)
        def add_task_args(x, y):
            return x + y

        # Without param.
        @celery.task
        def add_task_noargs(x, y):
            return x + y

        for task in add_task_args, add_task_noargs:
            # Sanity for task output.
            self.assertEqual(task(2, 2), 4)

            # Sanity for serializer content type.
            self.assertEqual(task.serializer, "json")

    def test_apply(self):
        # Apply async check.
        @celery.task
        def add(x, y):
            return x + y

        res = add.apply_async((16, 16))
        self.assertTrue(res.task_id)

    def test_Worker(self):
        # Check if worker exists.
        worker = celery.Worker()
        self.assertTrue(worker)