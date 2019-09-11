"""
This module includes all the punching_clock tasks.
"""

import logging

from factory import celery
from api.punching_clock.helpers.mail_helper import send_error_mail
from api.punching_clock.helpers.slack_helper import SlackUtil

logger = logging.getLogger('punching_clock')


@celery.task
def send_error_mail_c(sender, receivers, msg, subject):
    """Async task to send mail which internally calls send_error_mail method.

    Parameters
    ----------
    `sender` : <String>
        Sender address.

    `receivers` : <List>
        List of address intended to be notified.

    `msg` : <String>
        Message to be sent.

    `msg` : <String>
        Body of the email.

    `subject` : <String>
        Subject of the email.

    Returns
    -------
        <Boolean>: True in case of success else False.
    """

    return send_error_mail(sender, receivers, msg, subject)


@celery.task
def send_slack_notification_c(channel_id='#punching_clock-errors', message='Error', username='AttendanceClock BOT',
                              icon_emoji=':robot_face:'):
    """Async task to send slack notification of error.

    Parameters
    ----------
    `channel_id` : <String>
        Slack channel id.

    `message` : <List>
        Message to be sent.

    `username` : <String>
        Name of slack bot who will notify.

    `msg` : <String>
        Body of the email.

    `icon_emoji` : <String>
        Slack bot Avatar.

    Returns
    -------
        <Dict>: response dict.
        Sample success response:
        {
            "ok": True,
            "channel": "C1H9RESGL",
            "ts": "1503435956.000247",
            "message": {
                "text": "Some message",
                "username": "ecto1",
                "bot_id": "B19LU7CSY",
                "attachments": [
                    {
                        "text": "This is an attachment",
                        "id": 1,
                        "fallback": "This is an attachment's fallback"
                    }
                ],
                "type": "message",
                "subtype": "bot_message",
                "ts": "1503435956.000247"
            }
        }

        Sample error response:
        {
            "ok": False,
            "error": "too_many_attachments"
        }
    """

    return SlackUtil().send_message(channel_id=channel_id, message=message, username=username, icon_emoji=icon_emoji)
