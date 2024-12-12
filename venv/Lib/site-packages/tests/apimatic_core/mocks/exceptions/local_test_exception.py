from apimatic_core.utilities.api_helper import ApiHelper
from tests.apimatic_core.mocks.exceptions.global_test_exception import GlobalTestException


class LocalTestException(GlobalTestException):
    def __init__(self, reason, response):
        """Constructor for the LocalTestException class

        Args:
            reason (string): The reason (or error message) for the Exception
                to be raised.
            response (HttpResponse): The HttpResponse of the API call.

        """
        super(LocalTestException, self).__init__(reason, response)
        dictionary = ApiHelper.json_deserialize(self.response.text)
        if isinstance(dictionary, dict):
            self.unbox(dictionary)

    def unbox(self, dictionary):
        """Populates the properties of this object by extracting them from a dictionary.

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        """
        super(LocalTestException, self).unbox(dictionary)
        self.secret_message_for_endpoint = dictionary.get("SecretMessageForEndpoint") if dictionary.get("SecretMessageForEndpoint") else None
