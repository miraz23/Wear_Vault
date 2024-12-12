from apimatic_core_interfaces.types.authentication import Authentication

from apimatic_core.utilities.auth_helper import AuthHelper


class QueryAuth(Authentication):

    def __init__(self, auth_params):
        self._auth_params = auth_params

    def is_valid(self):
        return AuthHelper.is_valid_auth(self._auth_params)

    def apply(self, http_request):
        return AuthHelper.apply(self._auth_params, http_request.add_query_parameter)
