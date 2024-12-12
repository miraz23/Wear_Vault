from apimatic_core_interfaces.logger.api_logger import ApiLogger
from apimatic_core.constants.logger_constants import LoggerConstants

class SdkLogger(ApiLogger):

    def __init__(self, api_logging_configuration):
        """Default Constructor.

        Args:
            api_logging_configuration (ApiLoggingConfiguration): The Api logging configuration.
        """
        self._api_logging_config = api_logging_configuration
        self._logger = self._api_logging_config.logger
        self._level = self._api_logging_config.log_level
        self._mask_sensitive_headers = self._api_logging_config.mask_sensitive_headers
        self._request_logging_config = self._api_logging_config.request_logging_config
        self._response_logging_config = self._api_logging_config.response_logging_config

    def log_request(self, http_request):
        """Logs the given HTTP request.

        Args:
            http_request (HttpRequest): The HTTP request to log.
        """
        _lowered_case_headers = {key.lower(): value for key, value in http_request.headers.items()}
        _content_type = _lowered_case_headers.get(LoggerConstants.CONTENT_TYPE_HEADER)
        _url = self._request_logging_config.get_loggable_url(http_request.query_url)
        params = {
            LoggerConstants.METHOD: http_request.http_method,
            LoggerConstants.URL: _url,
            LoggerConstants.CONTENT_TYPE: _content_type,
        }

        self._logger.log(self._level, "Request %s %s %s", params)

        if self._request_logging_config.log_headers:
            self._logger.log(self._level, "Request Headers %s",
                             self._get_loggable_headers(self._request_logging_config, http_request.headers))

        if self._request_logging_config.log_body:
            body = http_request.parameters if http_request.parameters is not None else http_request.files
            params = {
                LoggerConstants.BODY: body
            }
            self._logger.log(self._level, "Request Body %s", params)

    def log_response(self, http_response):
        """Logs the given HTTP response.

        Args:
            http_response (HttpRequest): The HTTP request to log.
        """
        _lowered_case_headers = {key.lower(): value for key, value in http_response.headers.items()}
        _content_type = _lowered_case_headers.get(LoggerConstants.CONTENT_TYPE_HEADER)
        _content_length = _lowered_case_headers.get(LoggerConstants.CONTENT_LENGTH_HEADER)
        params = {
            LoggerConstants.STATUS_CODE: http_response.status_code,
            LoggerConstants.CONTENT_TYPE: _content_type,
            LoggerConstants.CONTENT_LENGTH: _content_length,
        }
        self._logger.log(self._level, "Response %s %s %s", params)

        if self._response_logging_config.log_headers:
            self._logger.log(self._level, "Response Headers %s",
                             self._get_loggable_headers(self._response_logging_config, http_response.headers))

        if self._response_logging_config.log_body:
            params = {
                LoggerConstants.BODY: http_response.text
            }
            self._logger.log(self._level, "Response Body %s", params)

    def _get_loggable_headers(self, logging_config, headers):
        return {
            LoggerConstants.HEADERS: logging_config.get_loggable_headers(headers, self._mask_sensitive_headers)
        }


class NoneSdkLogger(ApiLogger):

    def log_request(self, http_request):
        """Logs the given HTTP request.

        Args:
            http_request (HttpRequest): The HTTP request to log.
        """
        pass

    def log_response(self, http_response):
        """Logs the given HTTP response.

        Args:
            http_response (HttpRequest): The HTTP request to log.
        """
        pass


class LoggerFactory:

    @classmethod
    def get_api_logger(cls, api_logging_configuration):
        """Default Constructor.

        Args:
            api_logging_configuration (ApiLoggingConfiguration): The Api logging configuration.

        Returns:
            ApiLogger: The implementation of ApiLogger.
        """
        if api_logging_configuration is None:
            return NoneSdkLogger()

        return SdkLogger(api_logging_configuration)
