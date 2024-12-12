import base64
import calendar
from datetime import datetime


class AuthHelper:

    @staticmethod
    def get_base64_encoded_value(*props, delimiter=':'):
        if props.__len__() > 0 and not any(prop is None for prop in props):
            joined = delimiter.join(props)
            encoded = base64.b64encode(str.encode(joined)).decode('iso-8859-1')
            return encoded

    @staticmethod
    def get_token_expiry(current_timestamp, expires_in):
        return current_timestamp + int(expires_in)

    @staticmethod
    def get_current_utc_timestamp():
        return calendar.timegm(datetime.now().utctimetuple())

    @staticmethod
    def is_token_expired(token_expiry, clock_skew_time=None):
        """ Checks if OAuth token has expired.

        Returns:
            bool: True if token has expired, False otherwise.

        """
        if clock_skew_time is not None and token_expiry is not None:
            token_expiry -= clock_skew_time
        utc_now = AuthHelper.get_current_utc_timestamp()
        return token_expiry is not None and token_expiry < utc_now

    @staticmethod
    def is_valid_auth(auth_params):
        return auth_params and all(param and auth_params[param] for param in auth_params)

    @staticmethod
    def apply(auth_params, func):
        for param in auth_params:
            func(param, auth_params[param])
