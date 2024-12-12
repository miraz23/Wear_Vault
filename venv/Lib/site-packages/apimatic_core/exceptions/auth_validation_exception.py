"""
This is an exception class which will be raised when auth validation fails.
"""


class AuthValidationException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
