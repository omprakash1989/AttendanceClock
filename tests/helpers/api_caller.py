import logging
from datetime import datetime

from requests import api
from ..exceptions import APICallError

logger = logging.getLogger("punching_clock")


class APICaller(object):

    def call_api(self, method, url, raise_exception_on_error=True, **kwargs):
        logger.debug("request method is {} url is {} args are {}".format(method, url, kwargs))
        logger.debug("emitting pre_call_api signal")
        # Add if any precall signals are there.

        response = api.request(method, url, **kwargs)

        logger.debug("response of api request is {}".format(response))
        logger.debug("emitting post_call_api signal with args {}".format(kwargs))
        datetime_str = datetime.now()
        signal_arguments = {
            "method": method,
            "url": url,
            "datetime_str": datetime_str,
            "status_code": response.status_code,
            "response": response.text,
            "other": None
        }
        # data/json is included in kwargs

        # Add if any postcall signals are there.

        if raise_exception_on_error and response.status_code != 200:
            raise APICallError(response.status_code, response.text)

        return response
