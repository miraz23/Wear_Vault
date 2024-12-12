from apimatic_core_interfaces.types.authentication import Authentication


class Single(Authentication):

    @property
    def error_message(self):
        return "[{}]".format(self._error_message)

    def __init__(self, auth_participant):
        super(Single, self).__init__()
        self._auth_participant = auth_participant
        self._mapped_auth = None
        self._error_message = None
        self._is_valid = False

    def with_auth_managers(self, auth_managers):
        if not auth_managers.get(self._auth_participant):
            raise ValueError("Auth key is invalid.")

        self._mapped_auth = auth_managers[self._auth_participant]

        return self

    def is_valid(self):
        self._is_valid = self._mapped_auth.is_valid()
        if not self._is_valid:
            self._error_message = self._mapped_auth.error_message

        return self._is_valid

    def apply(self, http_request):

        if not self._is_valid:
            return

        self._mapped_auth.apply(http_request)

