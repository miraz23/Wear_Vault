from apimatic_core.configurations.endpoint_configuration import EndpointConfiguration
from apimatic_core.configurations.global_configuration import GlobalConfiguration
from apimatic_core.logger.sdk_logger import LoggerFactory
from apimatic_core.response_handler import ResponseHandler


class ApiCall:

    @property
    def new_builder(self):
        return ApiCall(self._global_configuration)

    def __init__(
            self,
            global_configuration=GlobalConfiguration()
    ):
        self._global_configuration = global_configuration
        self._request_builder = None
        self._response_handler = ResponseHandler()
        self._endpoint_configuration = EndpointConfiguration()
        self._api_logger = LoggerFactory.get_api_logger(self._global_configuration.get_http_client_configuration()
                                                        .logging_configuration)

    def request(self, request_builder):
        self._request_builder = request_builder
        return self

    def response(self, response_handler):
        self._response_handler = response_handler
        return self

    def endpoint_configuration(self, endpoint_configuration):
        self._endpoint_configuration = endpoint_configuration
        return self

    def execute(self):
        _http_client_configuration = self._global_configuration.get_http_client_configuration()

        if _http_client_configuration.http_client is None:
            raise ValueError("An HTTP client instance is required to execute an Api call.")

        _http_request = self._request_builder.build(self._global_configuration)

        # Logging the request
        self._api_logger.log_request(_http_request)

        _http_callback = _http_client_configuration.http_callback

        # Applying the on before sending HTTP request callback
        if _http_callback is not None:
            _http_callback.on_before_request(_http_request)

        # Executing the HTTP call
        _http_response = _http_client_configuration.http_client.execute(
            _http_request, self._endpoint_configuration)

        # Logging the response
        self._api_logger.log_response(_http_response)

        # Applying the after receiving HTTP response callback
        if _http_callback is not None:
            _http_callback.on_after_response(_http_response)

        return self._response_handler.handle(_http_response, self._global_configuration.get_global_errors())
