from apimatic_core.utilities.api_helper import ApiHelper
from tests.apimatic_core.mocks.exceptions.api_exception import APIException
from tests.apimatic_core.mocks.models.validate import Validate


class NestedModelException(APIException):
    def __init__(self, reason, response):
        """Constructor for the NestedModelException class

        Args:
            reason (string): The reason (or error message) for the Exception
                to be raised.
            response (HttpResponse): The HttpResponse of the API call.

        """
        super(NestedModelException, self).__init__(reason, response)
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
        self.server_message = dictionary.get("ServerMessage") if dictionary.get("ServerMessage") else None
        self.server_code = dictionary.get("ServerCode") if dictionary.get("ServerCode") else None
        self.model = Validate.from_dictionary(dictionary.get('model')) if dictionary.get('model') else None
