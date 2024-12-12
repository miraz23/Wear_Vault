from apimatic_core.authentication.multiple.auth_group import AuthGroup


class And(AuthGroup):

    @property
    def error_message(self):
        return " and ".join(self._error_messages)

    def __init__(self, *auth_group):
        super(And, self).__init__(auth_group)
        self._is_valid_group = True

    def is_valid(self):
        if not self.mapped_group:
            return False

        for participant in self.mapped_group:
            if not participant.is_valid():
                self.error_messages.append(participant.error_message)
                self._is_valid_group = False

        return self.is_valid_group
