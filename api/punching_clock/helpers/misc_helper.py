"""
This contains all utility methods which are generic and reusable.
"""

from functools import wraps
import smtplib
from pytz import timezone
from timezones import tz_utils

from settings import GEOIP_DATA_LOCATION

from flask import abort
from werkzeug.exceptions import BadRequest
from flask import request, Flask, abort, g
from urllib.parse import unquote

tz_utils.GEOIP_DATA_LOCATION = GEOIP_DATA_LOCATION


def check_positive(data):
    """
    Checking the given input is a positive integer or not.
    :param data: Integer    Input data
    :return: input in case of positive integer else 1.
    """
    if data and data > 0:
        return data
    else:
        return 1


def check_if_not_empty(data):
    """
    Check if a provided data is not empty.

    :param data: String/Integer
    Input data. Can be a string or Integer.

    :return:
    Returns validated data.

    :raises: TypeError and Value Error exception.
    """

    try:
        if data:
            return str(data)
        else:
            raise ValueError('Please provide valid input.')

    except (ValueError, TypeError):
        raise ValueError('Please provide valid input.')


def application_json_content_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        headers = request.headers
        content_verified = False
        if not headers:  # no header set
            abort(400, "Only application/json content type accepted.")

        if headers['Content-Type'] != 'application/json':
            abort(400, "Only application/json content type accepted.")

        return f(*args, **kwargs)

    return decorated


def update_global(data):
    """Update the flask-global `g` object with given data.

    Parameters
    ----------
    `data` : <dict>
        A k-v pair of values to update

    Returns
    -------
    None
    """
    for key, value in data.items():
        setattr(g, key, value)


def get_bool_value(value):
    """
    Get boolean value from a string.

    :param value: String/Integer
    Input value whose boolean value to be calculated.

    :return: Boolean
    Returns True or False.
    """

    bool_val = False

    if value:
        if isinstance(value, str):
            if value.lower() == 'true':
                bool_val = True

        elif isinstance(value, int):
            if value == 1:
                bool_val = True

    return bool_val


def send_mail(mailhost, mailport, sender, receivers, msg, username=None, password=None):

    """Send mails to recipients, specially designed to send error mails.

    Parameters
    ----------
    `mailhost` : <String>
        SMTP host

    `mailport` : <Integer>
        SMTP port

    `sender` : <String>
        Sender address.

    `receivers` : <List>
        List of address intended to be notified.

    `msg` : <String>
        Message to be sent.

    `username` : <String>
        SMTP username.

    `password` : <String>
        SMTP password.

    Returns
    -------
    None
    """

    smtp = smtplib.SMTP(mailhost, mailport)
    if username:
        # TLS handling.
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(username, password)

    # Send mail.
    smtp.sendmail(sender, receivers, msg)
    smtp.quit()


# Convert duration objects into human-readable form
def duration_to_plain_english(duration):
    duration_mins, duration_secs = divmod(duration.seconds, 60)
    duration_hours, duration_mins = divmod(duration_mins, 60)

    duration_text = ""

    if duration.days > 0:
        if duration.days == 1:
            duration_text += "1 day, "
        else:
            duration_text += str(duration.days) + " days, "

    if duration_hours > 0:
        if duration_hours == 1:
            duration_text += "1 hour, "
        else:
            duration_text += str(duration_hours) + " hours, "

    if duration_mins == 1:
        duration_text += "1 minute"
    else:
        duration_text += str(duration_mins) + " minutes"

    return duration_text


# Identify the user's time zone
def guess_user_timezone(user_ip):
    user_timezone_name = tz_utils.guess_timezone_by_ip(
            ip='202.189.245.114',
            only_name=True
            )
    import pdb;pdb.set_trace()
    user_timezone = timezone(user_timezone_name)
    return user_timezone
