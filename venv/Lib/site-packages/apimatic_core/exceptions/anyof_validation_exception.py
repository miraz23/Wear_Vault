"""
This is an exception class which will be raised when union type validation fails.
"""


class AnyOfValidationException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
