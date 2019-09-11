"""
Module unittests should be here.
"""


import unittest
import importlib

from flask import Flask

from api.punching_clock.helpers.mail_helper import send_error_mail
from settings import settings_local_sample, ENV
from api.punching_clock.helpers.slack_helper import SlackUtil


class TestAttendanceClockModules(unittest.TestCase):
    """
    Test case for punching_clock modules.
    """

    def setUp(self):
        pass

    def test_error_mail(self):
        """ Tests sending error mail module.

        :return: None
        """
        self.assertEqual(send_error_mail('om@test.com', ['om@test.com'], "Hi,\n\nThis is a test mail.",
                                         "Test Mail."), True)

    def test_slack_notification(self):
        """ Tests sending slack notification module.

        :return: None
        """

        resp = SlackUtil().send_message(message='Build Test Message', username='{} {}'.format('AttendanceClock BOT',
                                                                                              ENV.capitalize()))
        self.assertEqual(resp.get("ok", False), True)

    def test_settings_sanity_p1(self):
        """
        Check if all the environment settings have a sanity.
        :return:
        """

        fake_app = Flask('FakeApp')
        fail_msg = '{} does not match to settings_local_sample'

        # Get Sample Settings.
        fake_app.config.from_object(settings_local_sample)

        # Get count sample setting attributes.
        sample_setting_attr_count = fake_app.config.keys().__len__()

        # Check for all other setting modules.
        for mod in ['settings_staging', 'settings_docker']:
            # Import module.
            settings_mod = importlib.import_module('settings.{}'.format(mod))

            # Apply config.
            fake_app.config.from_object(settings_mod)

            # Assert setting module attributes count with the count of sample settings.
            self.assertEqual(fake_app.config.keys().__len__(), sample_setting_attr_count,
                             fail_msg.format(settings_mod.__name__))
