import pytest
import unittest
from api.punching_clock.tasks import send_error_mail_c, send_slack_notification_c
from settings import ENV


class TestTasks(unittest.TestCase):
    """
    Test the celery tasks.
    """

    @pytest.fixture(scope='session')
    def test_send_error_mail_c(self):
        """
        Test case for sending the error email.
        """

        # self.assertEqual(send_error_mail_c('om@test.com', ['om@test.com'], 'Celery Test Mail',
        #                                    'Celery Test Email'), True)
        pass

    @pytest.fixture(scope='session')
    def test_send_slack_notification_c(self):
        """
        Test case for sending the slack notifications.
        """

        slack_notification = send_slack_notification_c(message='Celery Test Message from {}'.format(ENV),
                                                       username='{} {}'.format('AttendanceClock BOT', ENV.capitalize()))
        # self.assertEqual(slack_notification.get("ok", False), True)
