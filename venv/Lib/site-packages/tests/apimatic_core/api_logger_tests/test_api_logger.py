import logging
import pytest

from apimatic_core_interfaces.types.http_method_enum import HttpMethodEnum
from apimatic_core.logger.sdk_logger import SdkLogger
from apimatic_core.request_builder import RequestBuilder
from apimatic_core.response_handler import ResponseHandler
from apimatic_core.types.parameter import Parameter
from apimatic_core.utilities.api_helper import ApiHelper
from tests.apimatic_core.base import Base
from tests.apimatic_core.mocks.callables.base_uri_callable import Server
from tests.apimatic_core.mocks.logger.api_logger import ApiLogger
from testfixtures import LogCapture

from tests.apimatic_core.mocks.models.person import Employee


class TestApiLogger(Base):

    @pytest.fixture
    def log_capture(self):
        """Fixture to capture logs during the test."""
        with LogCapture() as capture:
            yield capture

    def init_sdk_logger(self, logger, log_level=logging.INFO, mask_sensitive_headers=True,
                        request_logging_configuration=None,
                        response_logging_configuration=None):
        self._api_request = self.request(
            http_method=HttpMethodEnum.POST,
            query_url='http://localhost:3000/body/model?key=value',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'},
            parameters=ApiHelper.json_serialize({"Key": "Value"})
        )
        self._api_response = self.response(
            text=ApiHelper.json_serialize({"Key": "Value"}),
            headers={
                'Content-Type': 'application/json',
                'Content-Length': 50
            }
        )
        self._api_logger = self.get_api_logger(logger, log_level, mask_sensitive_headers, request_logging_configuration,
                                               response_logging_configuration)

    def get_api_logger(self, logger, log_level=logging.INFO, mask_sensitive_headers=True,
                       request_logging_configuration=None,
                       response_logging_configuration=None):
        return SdkLogger(self.api_logging_configuration(
            logger, log_level=log_level, mask_sensitive_headers=mask_sensitive_headers,
            request_logging_configuration=request_logging_configuration,
            response_logging_configuration=response_logging_configuration))

    def test_custom_logger_for_request(self, log_capture):
        self.init_sdk_logger(logger=ApiLogger())
        self._api_logger.log_request(self._api_request)
        # Assert the captured logs
        records = log_capture.records
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Request %s %s %s' and
                                     record.args == ('POST', 'http://localhost:3000/body/model', 'application/json') and
                                     record.message == 'Request POST http://localhost:3000/body/model application/json',
            max_checks=1)
        assert all(record.levelname == "INFO" for record in records)

    def test_custom_logger_for_request_with_log_level(self, log_capture):
        self.init_sdk_logger(logger=ApiLogger(), log_level=logging.WARN)
        self._api_logger.log_request(self._api_request)
        # Assert the captured logs
        records = log_capture.records
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Request %s %s %s' and
                                     record.args == ('POST', 'http://localhost:3000/body/model', 'application/json') and
                                     record.message == 'Request POST http://localhost:3000/body/model application/json',
            max_checks=1)
        assert all(record.levelname == "WARNING" for record in records)

    def test_custom_logger_for_request_with_include_query_in_path(self, log_capture):
        self.init_sdk_logger(logger=ApiLogger(),
                             request_logging_configuration=self.api_request_logging_configuration(
                                 include_query_in_path=True))
        self._api_logger.log_request(self._api_request)
        # Assert the captured logs
        records = log_capture.records
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Request %s %s %s' and
                                     record.args == ('POST', 'http://localhost:3000/body/model?key=value', 'application/json') and
                                     record.message == 'Request POST http://localhost:3000/body/model?key=value application/json',
            max_checks=1)
        assert all(record.levelname == "INFO" for record in records)

    def test_custom_logger_for_request_with_log_request_header(self, log_capture):
        self.init_sdk_logger(logger=ApiLogger(),
                             request_logging_configuration=self.api_request_logging_configuration(log_headers=True))
        self._api_logger.log_request(self._api_request)

        # Assert the captured logs
        records = log_capture.records
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Request %s %s %s' and
                                     record.args == ('POST', 'http://localhost:3000/body/model', 'application/json') and
                                     record.message == 'Request POST http://localhost:3000/body/model application/json',
            max_checks=1)
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Request Headers %s' and
                                     record.args == {'Content-Type': 'application/json', 'Accept': 'application/json'} and
                                     record.message == "Request Headers {'Content-Type': 'application/json', 'Accept': 'application/json'}",
            max_checks=1)
        assert all(record.levelname == "INFO" for record in records)

    def test_custom_logger_for_request_with_log_request_body(self, log_capture):
        self.init_sdk_logger(logger=ApiLogger(),
                             request_logging_configuration=self.api_request_logging_configuration(log_body=True))
        self._api_logger.log_request(self._api_request)

        # Assert the captured logs
        records = log_capture.records
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Request %s %s %s' and
                                     record.args == ('POST', 'http://localhost:3000/body/model', 'application/json') and
                                     record.message == 'Request POST http://localhost:3000/body/model application/json',
            max_checks=1)
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Request Body %s' and
                                     record.args == ('{"Key": "Value"}',) and
                                     record.message == 'Request Body {"Key": "Value"}',
            max_checks=1)
        assert all(record.levelname == "INFO" for record in records)

    def test_custom_logger_for_response(self, log_capture):
        self.init_sdk_logger(logger=ApiLogger())
        self._api_logger.log_response(self._api_response)
        # Assert the captured logs
        records = log_capture.records
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Response %s %s %s' and
                                     record.args == (200, 'application/json', 50) and
                                     record.message == 'Response 200 application/json 50',
            max_checks=1)
        assert all(record.levelname == "INFO" for record in records)

    def test_custom_logger_for_response_with_log_level(self, log_capture):
        self.init_sdk_logger(logger=ApiLogger(), log_level=logging.WARN)
        self._api_logger.log_response(self._api_response)
        # Assert the captured logs
        records = log_capture.records
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Response %s %s %s' and
                                     record.args == (200, 'application/json', 50) and
                                     record.message == 'Response 200 application/json 50',
            max_checks=1)
        assert all(record.levelname == "WARNING" for record in records)

    def test_custom_logger_for_response_with_log_response_header(self, log_capture):
        self.init_sdk_logger(logger=ApiLogger(),
                             response_logging_configuration=self.api_response_logging_configuration(log_headers=True))
        self._api_logger.log_response(self._api_response)

        # Assert the captured logs
        records = log_capture.records
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Response %s %s %s' and
                                     record.args == (200, 'application/json', 50) and
                                     record.message == 'Response 200 application/json 50',
            max_checks=1)
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Response Headers %s' and
                                     record.args == {'Content-Type': 'application/json', 'Content-Length': 50} and
                                     record.message == "Response Headers {'Content-Type': 'application/json', 'Content-Length': 50}",
            max_checks=1)
        assert all(record.levelname == "INFO" for record in records)

    def test_custom_logger_for_response_with_log_response_body(self, log_capture):
        self.init_sdk_logger(logger=ApiLogger(),
                             response_logging_configuration=self.api_response_logging_configuration(log_body=True))
        self._api_logger.log_response(self._api_response)

        # Assert the captured logs
        records = log_capture.records
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Response %s %s %s' and
                                     record.args == (200, 'application/json', 50) and
                                     record.message == 'Response 200 application/json 50',
            max_checks=1)
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Response Body %s' and
                                     record.args == ('{"Key": "Value"}',) and
                                     record.message == 'Response Body {"Key": "Value"}',
            max_checks=1)
        assert all(record.levelname == "INFO" for record in records)

    def test_custom_logger_for_end_to_end_api_call_test(self, log_capture):
        self.execute_api_call_with_logging(logger=ApiLogger())

        # Assert the captured logs
        records = log_capture.records
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Request %s %s %s' and
                                     record.args == ('POST', 'http://localhost:3000/body/model', 'application/json') and
                                     record.message == 'Request POST http://localhost:3000/body/model application/json',
            max_checks=1)
        assert self.any_with_limit(
            records,
            condition=lambda record: record.msg == 'Response %s %s %s' and
                                     record.args == (200, 'application/json', None) and
                                     record.message == 'Response 200 application/json None',
            max_checks=1)
        assert all(record.levelname == "INFO" for record in records)

    def execute_api_call_with_logging(self, logger):
        _api_call_builder = self.new_api_call_builder(self.global_configuration_with_logging(logger))
        _api_call_builder.new_builder \
            .request(RequestBuilder().server(Server.DEFAULT)
                     .path('/body/model')
                     .http_method(HttpMethodEnum.POST)
                     .header_param(Parameter()
                                   .key('Content-Type')
                                   .value('application/json'))
                     .body_param(Parameter()
                                 .value({"Key": "Value"})
                                 .is_required(True))
                     .query_param(Parameter()
                                  .key('accept')
                                  .value('application/json'))
                     .body_serializer(ApiHelper.json_serialize)
                     ) \
            .response(ResponseHandler()
                      .is_nullify404(True)
                      .deserializer(ApiHelper.json_deserialize)
                      .deserialize_into(Employee.from_dictionary)) \
            .execute()

    @staticmethod
    def any_with_limit(iterable, condition, max_checks):
        """Checks if any element in iterable meets the condition, with a limit on checks.

        Args:
            iterable: The iterable to check (list, string, etc.)
            condition: A function that takes an element and returns True if it meets the criteria.
            max_checks: The maximum number of elements to check before returning False (defaults to infinite).

        Returns:
            True if any element meets the condition within the check limit, False otherwise.
        """
        return sum(1 for element in iterable if condition(element)) == max_checks
