from flask import request, abort
from functools import wraps
from flask_httpauth import HTTPBasicAuth

from settings import CREDIT_LINE_API_AUTH, CIBIL_REPORT_API_AUTH

# Http basic auth.
auth = HTTPBasicAuth()


def requires_auth(**creds):
    def verify_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            authenticated = False
            if not auth:  # no header set
                abort(401, "Unauthorized access.")

            username = creds.get('username')
            password = creds.get('password')

            if username and password:
                if username == auth.username and password == auth.password:
                    authenticated = True

            if not authenticated:
                abort(401, "Unauthorized access.")
            return f(*args, **kwargs)

        return decorated
    return verify_auth


def requires_false_auth():
    """
    This is a so called auth decorator since this is the way it has been implemented in ADF.
    This is not a basic auth validator.

    :return:
    """

    def verify_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            headers = request.headers
            authenticated = False
            if headers:
                auth_key = headers.get('Authorization', None)

                if auth_key and auth_key == '{} {}'.format(CREDIT_LINE_API_AUTH['username'],
                                                           CREDIT_LINE_API_AUTH['password']):
                    authenticated = True

            if not authenticated:
                abort(401, "Unauthorized access.")
            return f(*args, **kwargs)

        return decorated
    return verify_auth


@auth.get_password
def get_pw(username):
    """Auth password retrieval.

    Parameters
    ----------
    `username`: <str>
        Username provided by the user.

    Returns
    -------
    <str>
        Password in case successful match of username.
    <None>
        In case username does not match.
    """
    if username == CIBIL_REPORT_API_AUTH['username']:
        return CIBIL_REPORT_API_AUTH['password']
    return None
