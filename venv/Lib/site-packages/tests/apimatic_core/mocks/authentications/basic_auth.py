from apimatic_core.authentication.header_auth import HeaderAuth
from apimatic_core.utilities.auth_helper import AuthHelper


class BasicAuth(HeaderAuth):

    @property
    def error_message(self):
        """Returns the auth specific error message"""
        return "BasicAuth: _basic_auth_user_name or _basic_auth_password is undefined."

    def __init__(self, basic_auth_user_name, basic_auth_password):
        auth_params = {}
        if basic_auth_user_name and basic_auth_password:
            auth_params = {'Basic-Authorization': "Basic {}".format(
                AuthHelper.get_base64_encoded_value(basic_auth_user_name, basic_auth_password))}
        super().__init__(auth_params=auth_params)
        self._basic_auth_user_name = basic_auth_user_name
        self._basic_auth_password = basic_auth_password
