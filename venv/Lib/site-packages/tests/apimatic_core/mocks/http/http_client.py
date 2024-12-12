from apimatic_core.factories.http_response_factory import HttpResponseFactory
from apimatic_core.http.response.http_response import HttpResponse
from apimatic_core_interfaces.client.http_client import HttpClient


class MockHttpClient(HttpClient):

    def __init__(self):
        self._should_retry = None
        self._contains_binary_response = None
        self.response_factory = HttpResponseFactory()

    def execute(self, request, endpoint_configuration):
        """Execute a given CoreHttpRequest to get a string response back

        Args:
            request (HttpRequest): The given HttpRequest to execute.
            endpoint_configuration (EndpointConfiguration): The endpoint configurations to use.

        Returns:
            HttpResponse: The response of the CoreHttpRequest.

        """
        self._should_retry = endpoint_configuration.should_retry
        self._contains_binary_response = endpoint_configuration.contains_binary_response
        return self.response_factory.create(status_code=200, reason=None,
                            headers=request.headers, body=str(request.parameters), request=request)

    def convert_response(self, response, contains_binary_response, http_request):
        """Converts the Response object of the CoreHttpClient into an
        CoreHttpResponse object.

        Args:
            response (dynamic): The original response object.
            contains_binary_response (bool): The flag to check if the response is of binary type.
            http_request (HttpRequest): The original HttpRequest object.

        Returns:
            CoreHttpResponse: The converted CoreHttpResponse object.

        """
        pass
