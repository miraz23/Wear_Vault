import re
from apimatic_core.utilities.api_helper import ApiHelper


class ErrorCase:

    def is_error_message_template(self):
        """Checks if the set exception message is a template or not.

            Returns:
                string: True if the exception message is a template.
            """
        return True if self._error_message_template else False

    def __init__(self):
        self._error_message = None
        self._error_message_template = None
        self._exception_type = None

    def error_message(self, error_message):
        """Setter for the error message.
            Args:
                error_message: The simple exception message.
            """
        self._error_message = error_message
        return self

    def error_message_template(self, error_message_template):
        """Setter for the error message template.
            Args:
                error_message_template: The exception message template containing placeholders.
            """
        self._error_message_template = error_message_template
        return self

    def exception_type(self, exception_type):
        """Setter for the exception type.
            Args:
                exception_type: The exception type to raise.
            """
        self._exception_type = exception_type
        return self

    def get_error_message(self, response):
        """Getter for the error message for the exception case. This considers both error message
        and error template message. Error message template has the higher precedence over an error message.
            Args:
                response: The received http response.

            Returns:
                string: The resolved exception message.
            """
        if self.is_error_message_template():
            return self._get_resolved_error_message_template(response)
        return self._error_message

    def raise_exception(self, response):
        """Raises the exception for the current error case type.
            Args:
                response: The received http response.
            """
        raise self._exception_type(self.get_error_message(response), response)

    def _get_resolved_error_message_template(self, response):
        """Updates all placeholders in the given message template with provided value.

                Args:
                    response: The received http response.

                Returns:
                    string: The resolved template value.
                """
        placeholders = re.findall(r'\{\$.*?\}', self._error_message_template)

        status_code_placeholder = set(filter(lambda element: element == '{$statusCode}', placeholders))
        header_placeholders = set(filter(lambda element: element.startswith('{$response.header'), placeholders))
        body_placeholders = set(filter(lambda element: element.startswith('{$response.body'), placeholders))

        # Handling response code placeholder
        error_message_template = ApiHelper.resolve_template_placeholders(status_code_placeholder,
                                                                         str(response.status_code),
                                                                         self._error_message_template)

        # Handling response header placeholder
        error_message_template = ApiHelper.resolve_template_placeholders(header_placeholders, response.headers,
                                                                         error_message_template)

        # Handling response body placeholder
        response_payload = ApiHelper.json_deserialize(response.text, as_dict=True)
        error_message_template = ApiHelper.resolve_template_placeholders_using_json_pointer(body_placeholders,
                                                                                            response_payload,
                                                                                            error_message_template)

        return error_message_template
