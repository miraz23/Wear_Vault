from apimatic_core.authentication.header_auth import HeaderAuth


class BearerAuth(HeaderAuth):

    @property
    def error_message(self):
        """Returns the auth specific error message"""
        return "BearerAuth: _access_token is undefined."

    def __init__(self, access_token):
        auth_params = {}
        if access_token:
            auth_params = {'Bearer-Authorization': "Bearer {}".format(access_token)}
        super().__init__(auth_params=auth_params)
        self._access_token = access_token
