"""
mail_helper

This module helps in handling mail related operations.
"""

import logging

from botocore.exceptions import ClientError

from settings import email_client

logger = logging.getLogger("punching_clock")


def send_error_mail(sender, receivers, msg, subject):

    """Send mails to recipients, specially designed to send error mails.

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
    None
    """

    charset = 'UTF-8'
    sent = False
    try:
        response = email_client.send_email(
            Destination={
                'ToAddresses': receivers,
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': charset,
                        'Data': msg,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            sent = True

    except ClientError as e:
        logger.exception("Boto client error while sending error emails: {}.".format(e.response['Error']['Message']))

    except Exception as exc:
        logger.exception("Exception while sending error emails: {}.".format(exc))

    return sent
