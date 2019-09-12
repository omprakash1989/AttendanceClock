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
        pass
        # self.assertEqual(send_error_mail('om@test.com', ['om@test.com'], "Hi,\n\nThis is a test mail.",
        #                                  "Test Mail."), True)

    def test_slack_notification(self):
        """ Tests sending slack notification module.

        :return: None
        """

        resp = SlackUtil().send_message(message='Build Test Message', username='{} {}'.format('AttendanceClock BOT',
                                                                                              ENV.capitalize()))
        # self.assertEqual(resp.get("ok", False), True)
