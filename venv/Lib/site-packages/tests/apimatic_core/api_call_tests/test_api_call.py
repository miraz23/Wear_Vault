import pytest
from apimatic_core.configurations.endpoint_configuration import EndpointConfiguration
from apimatic_core.request_builder import RequestBuilder
from apimatic_core.response_handler import ResponseHandler
from apimatic_core.types.parameter import Parameter
from apimatic_core.utilities.api_helper import ApiHelper
from apimatic_core_interfaces.types.http_method_enum import HttpMethodEnum
from tests.apimatic_core.base import Base
from tests.apimatic_core.mocks.callables.base_uri_callable import Server
from tests.apimatic_core.mocks.models.person import Employee


class TestApiCall(Base):

    def setup_test(self, global_config):
        self.global_config = global_config
        self.http_response_catcher = self.global_config.get_http_client_configuration().http_callback
        self.http_client = self.global_config.get_http_client_configuration().http_client
        self.api_call_builder = self.new_api_call_builder(self.global_config)

    def test_end_to_end_with_uninitialized_http_client(self):
        self.setup_test(self.default_global_configuration)
        with pytest.raises(ValueError) as exception:
            self.api_call_builder.new_builder.request(
                RequestBuilder().server(Server.DEFAULT)
                    .path('/body/model')
                    .http_method(HttpMethodEnum.POST)
                    .header_param(Parameter()
                                  .key('Content-Type')
                                  .value('application/json'))
                    .body_param(Parameter()
                                .value(Base.employee_model())
                                .is_required(True))
                    .header_param(Parameter()
                                  .key('accept')
                                  .value('application/json'))
                    .body_serializer(ApiHelper.json_serialize)
            ).response(
                ResponseHandler()
                    .is_nullify404(True)
                    .deserializer(ApiHelper.json_deserialize)
                    .deserialize_into(Employee.from_dictionary)
            ).execute()
        assert exception.value.args[0] == 'An HTTP client instance is required to execute an Api call.'

    def test_end_to_end_with_uninitialized_http_callback(self):
        self.setup_test(self.global_configuration_without_http_callback)
        actual_employee_model = self.api_call_builder.new_builder.request(
            RequestBuilder().server(Server.DEFAULT)
                .path('/body/model')
                .http_method(HttpMethodEnum.POST)
                .header_param(Parameter()
                              .key('Content-Type')
                              .value('application/json'))
                .body_param(Parameter()
                            .value(Base.employee_model())
                            .is_required(True))
                .header_param(Parameter()
                              .key('accept')
                              .value('application/json'))
                .body_serializer(ApiHelper.json_serialize)
        ).response(
            ResponseHandler()
                .is_nullify404(True)
                .deserializer(ApiHelper.json_deserialize)
                .deserialize_into(Employee.from_dictionary)
        ).execute()

        assert self.http_client._should_retry is None
        assert self.http_client._contains_binary_response is None
        assert self.http_response_catcher is None
        assert ApiHelper.json_serialize(Base.employee_model()) == ApiHelper.json_serialize(actual_employee_model)

    def test_end_to_end_with_not_implemented_http_callback(self):
        self.setup_test(self.global_configuration_unimplemented_http_callback)
        with pytest.raises(NotImplementedError) as not_implemented_exception:
            self.api_call_builder.new_builder.request(
                RequestBuilder().server(Server.DEFAULT)
                    .path('/body/model')
                    .http_method(HttpMethodEnum.POST)
                    .header_param(Parameter()
                                  .key('Content-Type')
                                  .value('application/json'))
                    .body_param(Parameter()
                                .value(Base.employee_model())
                                .is_required(True))
                    .header_param(Parameter()
                                  .key('accept')
                                  .value('application/json'))
                    .body_serializer(ApiHelper.json_serialize)
            ).response(
                ResponseHandler()
                    .is_nullify404(True)
                    .deserializer(ApiHelper.json_deserialize)
                    .deserialize_into(Employee.from_dictionary)
            ).execute()

        assert not_implemented_exception.value.args[0] == 'This method has not been implemented.'

    def test_end_to_end_without_endpoint_configurations(self):
        self.setup_test(self.global_configuration)
        actual_employee_model = self.api_call_builder.new_builder.request(
            RequestBuilder().server(Server.DEFAULT)
                .path('/body/model')
                .http_method(HttpMethodEnum.POST)
                .header_param(Parameter()
                              .key('Content-Type')
                              .value('application/json'))
                .body_param(Parameter()
                            .value(Base.employee_model())
                            .is_required(True))
                .header_param(Parameter()
                              .key('accept')
                              .value('application/json'))
                .body_serializer(ApiHelper.json_serialize)
        ).response(
            ResponseHandler()
                .is_nullify404(True)
                .deserializer(ApiHelper.json_deserialize)
                .deserialize_into(Employee.from_dictionary)
        ).execute()

        assert self.http_client._should_retry is None
        assert self.http_client._contains_binary_response is None
        assert self.http_response_catcher.response.status_code == 200
        assert ApiHelper.json_serialize(Base.employee_model()) == ApiHelper.json_serialize(actual_employee_model)

    @pytest.mark.parametrize('input_to_retry, '
                             'input_contains_binary_response, '
                             'expected_to_retry, expected_contains_binary_response', [
                                 (True, False, True, False),
                                 (False, True, False, True),
                                 (False, False, False, False),
                                 (True, True, True, True)
                             ])
    def test_end_to_end_with_endpoint_configurations(self, input_to_retry, input_contains_binary_response,
                                                     expected_to_retry, expected_contains_binary_response):
        self.setup_test(self.global_configuration)
        actual_employee_model = self.api_call_builder.new_builder.request(
            RequestBuilder().server(Server.DEFAULT)
                .path('/body/model')
                .http_method(HttpMethodEnum.POST)
                .header_param(Parameter()
                              .key('Content-Type')
                              .value('application/json'))
                .body_param(Parameter()
                            .value(Base.employee_model())
                            .is_required(True))
                .header_param(Parameter()
                              .key('accept')
                              .value('application/json'))
                .body_serializer(ApiHelper.json_serialize)
        ).response(
            ResponseHandler()
                .is_nullify404(True)
                .deserializer(ApiHelper.json_deserialize)
                .deserialize_into(Employee.from_dictionary)
        ).endpoint_configuration(
            EndpointConfiguration()
                .to_retry(input_to_retry)
                .has_binary_response(input_contains_binary_response)
        ).execute()

        assert self.http_client._should_retry == expected_to_retry
        assert self.http_client._contains_binary_response == expected_contains_binary_response
        assert self.http_response_catcher.response.status_code == 200
        assert ApiHelper.json_serialize(Base.employee_model()) == ApiHelper.json_serialize(actual_employee_model)
