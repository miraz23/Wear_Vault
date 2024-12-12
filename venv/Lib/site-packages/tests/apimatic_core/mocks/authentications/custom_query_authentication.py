from apimatic_core.authentication.query_auth import QueryAuth


class CustomQueryAuthentication(QueryAuth):

    @property
    def error_message(self):
        """Returns the auth specific error message"""
        return "CustomQueryAuthentication: _token or _api_key is undefined."

    def __init__(self, token, api_key):
        auth_params = {}
        if token and api_key:
            auth_params = {'token': token, 'api-key': api_key}
        super().__init__(auth_params=auth_params)
        self._token = token
        self._api_key = api_key

