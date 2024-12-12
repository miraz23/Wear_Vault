from apimatic_core_interfaces.types.authentication import Authentication

from apimatic_core.utilities.auth_helper import AuthHelper


class HeaderAuth(Authentication):

    def __init__(self, auth_params):
        self._auth_params = auth_params
        self._error_message = None

    def is_valid(self):
        return AuthHelper.is_valid_auth(self._auth_params)

    def apply(self, http_request):
        AuthHelper.apply(self._auth_params, http_request.add_header)

