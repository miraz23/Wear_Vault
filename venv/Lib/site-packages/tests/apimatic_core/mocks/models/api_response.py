from apimatic_core.http.response.api_response import ApiResponse
from apimatic_core.http.response.http_response import HttpResponse


class ApiResponse(ApiResponse):
    """Http response received.

    Attributes:
        status_code (int): The status code response from the server that
            corresponds to this response.
        reason_phrase (string): The reason phrase returned by the server.
        headers (dict): A dictionary of headers (key : value) that were
            returned with the response
        text (string): The Raw body of the HTTP Response as a string
        request (HttpRequest): The request that resulted in this response.
        body (Object): The data field specified for the response
        errors (Array<String>): Any errors returned by the server

    """

    def __init__(self, http_response,
                 body=None,
                 errors=None):
        """The Constructor

        Args:
            http_response (HttpResponse): The original, raw response from the api
            data (Object): The data field specified for the response
            errors (Array<String>): Any errors returned by the server

        """

        super().__init__(http_response, body, errors)
        if type(self.body) is dict:
            self.cursor = self.body.get('cursor')

    def __repr__(self):
        return '<Test ApiResponse [%s]>' % self.text

    @staticmethod
    def create(_parent_instance):
        return ApiResponse(
            HttpResponse(_parent_instance.status_code, _parent_instance.reason_phrase, _parent_instance.headers,
                         _parent_instance.text, _parent_instance.request), _parent_instance.body,
            _parent_instance.errors)
