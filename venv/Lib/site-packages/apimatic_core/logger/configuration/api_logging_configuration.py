import logging

from apimatic_core_interfaces.logger.logger import Logger

from apimatic_core.constants.logger_constants import LoggerConstants
from apimatic_core.logger.default_logger import ConsoleLogger
from apimatic_core.utilities.api_helper import ApiHelper


class ApiLoggingConfiguration:

    @property
    def logger(self):
        return self._logger

    @property
    def log_level(self):
        return self._log_level

    @property
    def mask_sensitive_headers(self):
        return self._mask_sensitive_headers

    @property
    def request_logging_config(self):
        return self._request_logging_config

    @property
    def response_logging_config(self):
        return self._response_logging_config

    def __init__(self, logger, log_level, mask_sensitive_headers,
                 request_logging_config, response_logging_config):
        """Default constructor.

        Args:
            logger (Logger): The logger implementation to log with.
            log_level (LogLevel): The log level to apply to the log message.
            mask_sensitive_headers (bool): Flag to control masking of sensitive headers.
            request_logging_config (ApiRequestLoggingConfiguration): The API request logging configuration.
            response_logging_config (ApiResponseLoggingConfiguration): The API response logging configuration.
        """

        self._logger = ConsoleLogger() if logger is None else logger
        self._log_level = logging.INFO if log_level is None else log_level
        self._mask_sensitive_headers = mask_sensitive_headers
        self._request_logging_config = request_logging_config
        self._response_logging_config = response_logging_config


class BaseHttpLoggingConfiguration:

    @property
    def log_body(self):
        return self._log_body

    @property
    def log_headers(self):
        return self._log_headers

    @property
    def headers_to_include(self):
        return self._headers_to_include

    @property
    def headers_to_exclude(self):
        return self._headers_to_exclude

    @property
    def headers_to_unmask(self):
        return self._headers_to_unmask

    def __init__(self, log_body, log_headers, headers_to_include,
                 headers_to_exclude, headers_to_unmask):
        """Default constructor.

        Args:
            log_body (bool): Controls the logging of the request body.
            log_headers (bool): Controls the logging of request headers.
            headers_to_include (List[str]): Includes only specified headers in the log output.
            headers_to_exclude (List[str]): Excludes specified headers from the log output.
            headers_to_unmask (List[str]): Logs specified headers without masking, revealing their actual values.
        """

        self._log_body = log_body
        self._log_headers = log_headers
        self._headers_to_include = [] if headers_to_include is None else ApiHelper.to_lower_case(headers_to_include)
        self._headers_to_exclude = [] if headers_to_exclude is None else ApiHelper.to_lower_case(headers_to_exclude)
        self._headers_to_unmask = [] if headers_to_unmask is None else ApiHelper.to_lower_case(headers_to_unmask)

    def get_loggable_headers(self, headers, mask_sensitive_headers):
        """
        Retrieves the headers to be logged based on the provided logging configuration,
        headers, and sensitivity masking configuration.

        Args:
            headers (Dict[str, str]): The headers to be evaluated for logging.
            mask_sensitive_headers (bool): Determines whether sensitive headers should be
                                            masked in the log.

        Returns:
            Dict[str, str]: A map containing the headers to be logged, considering the provided
                            configuration and sensitivity masking.
        """
        extracted_headers = self._extract_headers_to_log(headers)

        return self._mask_sensitive_headers(extracted_headers, mask_sensitive_headers)

    def _extract_headers_to_log(self, headers):
        """
        Extracts headers to log based on inclusion and exclusion criteria.

        Args:
            headers (Dict[str, str]): The map of headers.

        Returns:
            Dict[str, str]: The extracted headers to log.
        """
        if self.headers_to_include:
            return self._filter_included_headers(headers)
        if self.headers_to_exclude:
            return self._filter_excluded_headers(headers)

        return headers

    def _mask_sensitive_headers(self, headers, mask_sensitive_headers):
        """
        Masks sensitive headers from the given list of request headers.

        Args:
            headers (Dict[str, str]): The list of headers to filter.
            mask_sensitive_headers (bool): Whether to mask sensitive headers or not.

        Returns:
            Dict[str, str]: A map containing filtered headers.
        """
        if not mask_sensitive_headers:
            return headers

        filtered_headers = {}
        for key, value in headers.items():
            header_key = key.lower()
            is_non_sensitive = (header_key in LoggerConstants.NON_SENSITIVE_HEADERS or
                                header_key in self.headers_to_unmask)
            filtered_headers[key] = value if is_non_sensitive else "**Redacted**"

        return filtered_headers

    def _filter_included_headers(self, headers):
        """
        Filters headers to log based on inclusion criteria.

        Args:
            headers (Dict[str, str]): The map of headers.

        Returns:
            Dict[str, str]: The extracted headers to log.
        """
        extracted_headers = {}
        for key, value in headers.items():
            if key.lower() in self.headers_to_include:
                extracted_headers[key] = value
        return extracted_headers

    def _filter_excluded_headers(self, headers):
        """
        Filters headers to log based on exclusion criteria.

        Args:
            headers (Dict[str, str]): The map of headers.

        Returns:
            Dict[str, str]: The extracted headers to log.
        """
        extracted_headers = {}
        for key, value in headers.items():
            if key.lower() not in self.headers_to_exclude:
                extracted_headers[key] = value
        return extracted_headers


class ApiRequestLoggingConfiguration(BaseHttpLoggingConfiguration):

    @property
    def include_query_in_path(self):
        return self._include_query_in_path

    def __init__(self, log_body, log_headers, headers_to_include,
                 headers_to_exclude, headers_to_unmask,
                 include_query_in_path):
        """Default constructor.

        Args:
            log_body (bool): Controls the logging of the request body.
            log_headers (bool): Controls the logging of request headers.
            headers_to_include (List[str]): Includes only specified headers in the log output.
            headers_to_exclude (List[str]): Excludes specified headers from the log output.
            headers_to_unmask (List[str]): Logs specified headers without masking, revealing their actual values.
            include_query_in_path (bool): Determines whether to include query parameters in the logged request path.
        """
        super(ApiRequestLoggingConfiguration, self).__init__(log_body, log_headers, headers_to_include,
                                                             headers_to_exclude, headers_to_unmask)
        self._include_query_in_path = include_query_in_path

    def get_loggable_url(self, query_url):
        """
        Retrieves a URL suitable for logging purposes.

        This method determines the URL to be logged based on the `include_query_in_path` configuration.

        Args:
            query_url (str): The original URL containing query parameters.

        Returns:
            str: The URL to be logged.
                - If `include_query_in_path` is True, the original URL with query parameters is returned.
                - If `include_query_in_path` is False (default), the URL without query parameters is returned.
        """
        if self.include_query_in_path:
            return query_url

        return ApiHelper.get_url_without_query(query_url)


class ApiResponseLoggingConfiguration(BaseHttpLoggingConfiguration):

    def __init__(self, log_body, log_headers, headers_to_include,
                 headers_to_exclude, headers_to_unmask):
        """Default constructor.

        Args:
            log_body (bool): Controls the logging of the request body.
            log_headers (bool): Controls the logging of request headers.
            headers_to_include (List[str]): Includes only specified headers in the log output.
            headers_to_exclude (List[str]): Excludes specified headers from the log output.
            headers_to_unmask (List[str]): Logs specified headers without masking, revealing their actual values.
        """

        super(ApiResponseLoggingConfiguration, self).__init__(log_body, log_headers, headers_to_include,
                                                              headers_to_exclude, headers_to_unmask)
