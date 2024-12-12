import logging
import os
import platform
from datetime import datetime, date

from apimatic_core.api_call import ApiCall
from apimatic_core.http.configurations.http_client_configuration import HttpClientConfiguration
from apimatic_core.http.http_callback import HttpCallBack
from apimatic_core.logger.configuration.api_logging_configuration import ApiLoggingConfiguration, \
    ApiRequestLoggingConfiguration, ApiResponseLoggingConfiguration
from apimatic_core.utilities.api_helper import ApiHelper
from apimatic_core_interfaces.types.http_method_enum import HttpMethodEnum
from apimatic_core.configurations.global_configuration import GlobalConfiguration
from apimatic_core.http.request.http_request import HttpRequest
from apimatic_core.http.response.http_response import HttpResponse
from apimatic_core.request_builder import RequestBuilder
from apimatic_core.response_handler import ResponseHandler
from apimatic_core.types.error_case import ErrorCase
from tests.apimatic_core.mocks.authentications.basic_auth import BasicAuth
from tests.apimatic_core.mocks.authentications.bearer_auth import BearerAuth
from tests.apimatic_core.mocks.authentications.custom_header_authentication import CustomHeaderAuthentication
from tests.apimatic_core.mocks.authentications.custom_query_authentication import CustomQueryAuthentication
from tests.apimatic_core.mocks.exceptions.global_test_exception import GlobalTestException
from tests.apimatic_core.mocks.exceptions.nested_model_exception import NestedModelException
from tests.apimatic_core.mocks.http.http_response_catcher import HttpResponseCatcher
from tests.apimatic_core.mocks.http.http_client import MockHttpClient
from tests.apimatic_core.mocks.models.cat_model import CatModel
from tests.apimatic_core.mocks.models.complex_type import ComplexType
from tests.apimatic_core.mocks.models.dog_model import DogModel
from tests.apimatic_core.mocks.models.inner_complex_type import InnerComplexType
from tests.apimatic_core.mocks.models.one_of_xml import OneOfXML
from tests.apimatic_core.mocks.models.union_type_scalar_model import UnionTypeScalarModel
from tests.apimatic_core.mocks.models.wolf_model import WolfModel
from tests.apimatic_core.mocks.models.xml_model import XMLModel
from tests.apimatic_core.mocks.models.days import Days
from tests.apimatic_core.mocks.models.person import Employee, Person
from tests.apimatic_core.mocks.callables.base_uri_callable import Server, BaseUriCallable


class Base:

    @staticmethod
    def employee_model():
        return Employee(name='Bob', uid=1234567, address='street abc', department='IT', birthday=str(date(1994, 2, 13)),
                        birthtime=datetime(1994, 2, 13, 5, 30, 15), age=27,
                        additional_properties={'key1': 'value1', 'key2': 'value2'},
                        hired_at=datetime(1994, 2, 13, 5, 30, 15), joining_day=Days.MONDAY,
                        working_days=[Days.MONDAY, Days.TUESDAY], salary=30000,
                        dependents=[Person(name='John',
                                           uid=7654321,
                                           address='street abc',
                                           birthday=str(date(1994, 2, 13)),
                                           birthtime=datetime(1994, 2, 13, 5, 30, 15),
                                           age=12,
                                           additional_properties={'key1': 'value1', 'key2': 'value2'})])

    @staticmethod
    def employee_model_additional_dictionary():
        return Employee(name='Bob', uid=1234567, address='street abc', department='IT', birthday=str(date(1994, 2, 13)),
                        birthtime=datetime(1994, 2, 13, 5, 30, 15), age=27,
                        additional_properties={'key1': 'value1', 'key2': 'value2'},
                        hired_at=datetime(1994, 2, 13, 5, 30, 15), joining_day=Days.MONDAY,
                        working_days=[Days.MONDAY, Days.TUESDAY], salary=30000,
                        dependents=[Person(name='John',
                                           uid=7654321,
                                           address='street abc',
                                           birthday=str(date(1994, 2, 13)),
                                           birthtime=datetime(1994, 2, 13, 5, 30, 15),
                                           age=12,
                                           additional_properties={
                                               'key1': {'inner_key1': 'inner_val1', 'inner_key2': 'inner_val2'},
                                               'key2': ['value2', 'value3']})])

    @staticmethod
    def get_employee_dictionary():
        return {"address": "street abc", "age": 27, "birthday": "1994-02-13",
                "birthtime": Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)),
                "department": "IT", "dependents": [{"address": "street abc", "age": 12, "birthday": "1994-02-13",
                                                    "birthtime": Base.get_rfc3339_datetime(
                                                        datetime(1994, 2, 13, 5, 30, 15)),
                                                    "name": "John", "uid": 7654321, "personType": "Per",
                                                    "key1": "value1", "key2": "value2"}],
                "hiredAt": Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)),
                "joiningDay": "Monday", "name": "Bob", "salary": 30000, "uid": 1234567,
                "workingDays": ["Monday", "Tuesday"], "personType": "Empl"}

    @staticmethod
    def basic_auth():
        return BasicAuth(basic_auth_user_name='test_username', basic_auth_password='test_password')

    @staticmethod
    def bearer_auth():
        return BearerAuth(access_token='0b79bab50daca910b000d4f1a2b675d604257e42')

    @staticmethod
    def custom_header_auth():
        return CustomHeaderAuthentication(token='Qaws2W233WedeRe4T56G6Vref2')

    @staticmethod
    def custom_query_auth():
        return CustomQueryAuthentication(api_key='W233WedeRe4T56G6Vref2', token='Qaws2W233WedeRe4T56G6Vref2')

    @staticmethod
    def xml_model():
        return XMLModel(string_attr='String', number_attr=10000, boolean_attr=False,
                        string_element='Hey! I am being tested.', number_element=5000,
                        boolean_element=False, elements=['a', 'b', 'c'])

    @staticmethod
    def one_of_xml_dog_model():
        return OneOfXML(value=DogModel(barks=True))

    @staticmethod
    def one_of_xml_cat_model():
        return OneOfXML(value=[CatModel(meows=True), CatModel(meows=False)])

    @staticmethod
    def one_of_xml_wolf_model():
        return OneOfXML(value=[WolfModel(howls=True), WolfModel(howls=False)])

    @staticmethod
    def read_file(file_name):
        real_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        file_path = os.path.join(real_path, 'apimatic_core', 'mocks/files', file_name)
        return open(file_path, "rb")

    @staticmethod
    def global_errors():
        return {
            '400': ErrorCase().error_message('400 Global').exception_type(GlobalTestException),
            '412': ErrorCase().error_message('Precondition Failed').exception_type(NestedModelException),
            '3XX': ErrorCase().error_message('3XX Global').exception_type(GlobalTestException),
            'default': ErrorCase().error_message('Invalid response').exception_type(GlobalTestException),
        }

    @staticmethod
    def global_errors_with_template_message():
        return {
            '400': ErrorCase()
            .error_message_template('error_code => {$statusCode}, header => {$response.header.accept}, '
                                    'body => {$response.body#/ServerCode} - {$response.body#/ServerMessage}')
            .exception_type(GlobalTestException),
            '412': ErrorCase()
            .error_message_template('global error message -> error_code => {$statusCode}, header => '
                                    '{$response.header.accept}, body => {$response.body#/ServerCode} - '
                                    '{$response.body#/ServerMessage} - {$response.body#/model/name}')
            .exception_type(NestedModelException)
        }

    @staticmethod
    def request(http_method=HttpMethodEnum.GET,
                query_url='http://localhost:3000/test',
                headers=None,
                query_parameters=None,
                parameters=None,
                files=None):
        return HttpRequest(http_method=http_method,
                           query_url=query_url,
                           headers=headers,
                           query_parameters=query_parameters,
                           parameters=parameters,
                           files=files)

    @staticmethod
    def response(status_code=200, reason_phrase=None, headers=None, text=None):
        return HttpResponse(status_code=status_code, reason_phrase=reason_phrase,
                            headers=headers, text=text, request=Base.request())

    @staticmethod
    def get_http_datetime(datetime_value, should_return_string=True):
        if should_return_string is True:
            return ApiHelper.HttpDateTime.from_datetime(datetime_value)
        return ApiHelper.HttpDateTime(datetime_value)

    @staticmethod
    def get_rfc3339_datetime(datetime_value, should_return_string=True):
        if should_return_string is True:
            return ApiHelper.RFC3339DateTime.from_datetime(datetime_value)
        return ApiHelper.RFC3339DateTime(datetime_value)

    @staticmethod
    def new_api_call_builder(global_configuration):
        return ApiCall(global_configuration)

    @staticmethod
    def user_agent():
        return 'Python|31.8.0|{engine}|{engine-version}|{os-info}'

    @staticmethod
    def user_agent_parameters():
        return {
            'engine': {'value': platform.python_implementation(), 'encode': False},
            'engine-version': {'value': "", 'encode': False},
            'os-info': {'value': platform.system(), 'encode': False},
        }

    @staticmethod
    def wrapped_parameters():
        return {
            'bodyScalar': True,
            'bodyNonScalar': Base.employee_model(),
        }

    @staticmethod
    def mocked_http_client():
        return MockHttpClient()

    @staticmethod
    def http_client_configuration(http_callback=HttpResponseCatcher(), logging_configuration=None):
        http_client_configurations = HttpClientConfiguration(http_call_back=http_callback,
                                                             logging_configuration=logging_configuration)
        http_client_configurations.set_http_client(Base.mocked_http_client())
        return http_client_configurations

    @property
    def new_request_builder(self):
        return RequestBuilder().path('/test') \
            .server(Server.DEFAULT)

    @property
    def new_response_handler(self):
        return ResponseHandler()

    @property
    def global_configuration(self):
        return GlobalConfiguration(self.http_client_configuration()) \
            .base_uri_executor(BaseUriCallable().get_base_uri) \
            .global_errors(self.global_errors())

    @property
    def global_configuration_without_http_callback(self):
        return GlobalConfiguration(self.http_client_configuration(None)) \
            .base_uri_executor(BaseUriCallable().get_base_uri)

    @property
    def global_configuration_unimplemented_http_callback(self):
        return GlobalConfiguration(self.http_client_configuration(HttpCallBack())) \
            .base_uri_executor(BaseUriCallable().get_base_uri)

    @property
    def default_global_configuration(self):
        return GlobalConfiguration()

    @property
    def global_configuration_with_useragent(self):
        return self.global_configuration \
            .user_agent(self.user_agent(), self.user_agent_parameters())

    @property
    def global_configuration_with_auth(self):
        return self.global_configuration.auth_managers(
            {'basic_auth': self.basic_auth(), 'bearer_auth': self.bearer_auth(),
             'custom_header_auth': self.custom_header_auth(), 'custom_query_auth': self.custom_query_auth()})

    @staticmethod
    def api_request_logging_configuration(log_body=False, log_headers=False, headers_to_include=None,
                                          headers_to_exclude=None, headers_to_unmask=None,
                                          include_query_in_path=False):
        return ApiRequestLoggingConfiguration(log_body=log_body, log_headers=log_headers,
                                              headers_to_include=headers_to_include,
                                              headers_to_exclude=headers_to_exclude,
                                              headers_to_unmask=headers_to_unmask,
                                              include_query_in_path=include_query_in_path)

    @staticmethod
    def api_response_logging_configuration(log_body=False, log_headers=False, headers_to_include=None,
                                           headers_to_exclude=None, headers_to_unmask=None):
        return ApiResponseLoggingConfiguration(log_body=log_body, log_headers=log_headers,
                                               headers_to_include=headers_to_include,
                                               headers_to_exclude=headers_to_exclude,
                                               headers_to_unmask=headers_to_unmask)

    @staticmethod
    def api_logging_configuration(logger, log_level=logging.INFO, mask_sensitive_headers=True,
                                  request_logging_configuration=None,
                                  response_logging_configuration=None):
        if request_logging_configuration is None:
            request_logging_configuration = Base.api_request_logging_configuration()

        if response_logging_configuration is None:
            response_logging_configuration = Base.api_response_logging_configuration()

        return ApiLoggingConfiguration(logger, log_level, mask_sensitive_headers,
                                       request_logging_configuration,
                                       response_logging_configuration)

    @staticmethod
    def global_configuration_with_logging(logger):
        return GlobalConfiguration(Base.http_client_configuration(
            logging_configuration=Base.api_logging_configuration(logger))) \
            .base_uri_executor(BaseUriCallable().get_base_uri)

    @property
    def global_configuration_with_uninitialized_auth_params(self):
        return self.global_configuration.auth_managers(
            {'basic_auth': BasicAuth(None, None), 'bearer_auth': BearerAuth(None),
             'custom_header_auth': CustomHeaderAuthentication(None)})

    @property
    def global_configuration_with_partially_initialized_auth_params(self):
        return self.global_configuration.auth_managers(
            {'basic_auth': BasicAuth(None, None), 'custom_header_auth': self.custom_header_auth()})

    @staticmethod
    def get_complex_type():
        inner_complex_type = InnerComplexType(boolean_type=True,
                                              long_type=100003,
                                              string_type='abc',
                                              precision_type=55.44,
                                              string_list_type=['item1', 'item2'],
                                              additional_properties={'key0': 'abc', 'key1': 400})

        return ComplexType(inner_complex_type=inner_complex_type,
                           inner_complex_list_type=[inner_complex_type, inner_complex_type],
                           inner_complex_list_of_map_type=[{'key0': inner_complex_type, 'key1': inner_complex_type}],
                           inner_complex_map_type={'key0': inner_complex_type, 'key1': inner_complex_type},
                           inner_complex_map_of_list_type={'key0': [inner_complex_type, inner_complex_type],
                                                           'key2': [inner_complex_type, inner_complex_type]},
                           additional_properties={'prop1': [1, 2, 3], 'prop2': {'key0': 'abc', 'key1': 'def'}})

    @staticmethod
    def get_union_type_scalar_model():
        return UnionTypeScalarModel(any_of_required=1.5,
                                    one_of_req_nullable='abc',
                                    one_of_optional=200,
                                    any_of_opt_nullable=True)
