from apimatic_core.authentication.header_auth import HeaderAuth


class CustomHeaderAuthentication(HeaderAuth):

    @property
    def error_message(self):
        """Returns the auth specific error message"""
        return "CustomHeaderAuthentication: token is undefined."

    def __init__(self, token):
        auth_params = {}
        if token:
            auth_params = {'token': token}
        super().__init__(auth_params=auth_params)
        self._token = token
