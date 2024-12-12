from apimatic_core_interfaces.types.authentication import Authentication
from apimatic_core.authentication.multiple.single_auth import Single


class AuthGroup(Authentication):

    @property
    def auth_participants(self):
        return self._auth_participants

    @property
    def mapped_group(self):
        return self._mapped_group

    @property
    def error_messages(self):
        return self._error_messages

    @property
    def is_valid_group(self):
        return self._is_valid_group

    def __init__(self, auth_group):
        self._auth_participants = []
        for auth_participant in auth_group:
            if auth_participant is not None and isinstance(auth_participant, str):
                self._auth_participants.append(Single(auth_participant))
            elif auth_participant is not None:
                self._auth_participants.append(auth_participant)

        self._mapped_group = []
        self._error_messages = []
        self._is_valid_group = None

    def with_auth_managers(self, auth_managers):
        for participant in self.auth_participants:
            self.mapped_group.append(participant.with_auth_managers(auth_managers))

        return self

    def is_valid(self):  # pragma: no cover
        ...

    def apply(self, http_request):
        if not self.is_valid_group:
            return

        for participant in self.mapped_group:
            participant.apply(http_request)
