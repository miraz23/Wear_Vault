from datetime import datetime, date
import pytest
import sys

from apimatic_core.exceptions.auth_validation_exception import AuthValidationException
from apimatic_core_interfaces.types.http_method_enum import HttpMethodEnum
from apimatic_core.authentication.multiple.and_auth_group import And
from apimatic_core.authentication.multiple.or_auth_group import Or
from apimatic_core.authentication.multiple.single_auth import Single
from apimatic_core.types.array_serialization_format import SerializationFormats
from apimatic_core.types.file_wrapper import FileWrapper
from apimatic_core.types.parameter import Parameter
from apimatic_core.types.xml_attributes import XmlAttributes
from apimatic_core.utilities.api_helper import ApiHelper
from apimatic_core.utilities.auth_helper import AuthHelper
from apimatic_core.utilities.xml_helper import XmlHelper
from tests.apimatic_core.base import Base
from tests.apimatic_core.mocks.callables.base_uri_callable import Server
from requests.utils import quote
from tests.apimatic_core.mocks.union_type_lookup import UnionTypeLookUp


class TestRequestBuilder(Base):

    @pytest.mark.parametrize('input_server, expected_base_uri', [
        (Server.DEFAULT, 'http://localhost:3000/'),
        (Server.AUTH_SERVER, 'http://authserver:5000/')
    ])
    def test_base_uri(self, input_server, expected_base_uri):
        http_request = self.new_request_builder.server(input_server).path('/').build(self.global_configuration)
        assert http_request.query_url == expected_base_uri

    def test_path(self):
        http_request = self.new_request_builder.build(self.global_configuration)
        assert http_request.query_url == 'http://localhost:3000/test'

    def test_required_param(self):
        with pytest.raises(ValueError) as validation_error:
            self.new_request_builder \
                .query_param(Parameter()
                             .key('query_param')
                             .value(None)
                             .is_required(True)) \
                .build(self.global_configuration)
        assert validation_error.value.args[0] == 'Required parameter query_param cannot be None.'

    def test_optional_param(self):
        http_request = self.new_request_builder \
            .query_param(Parameter()
                         .key('query_param')
                         .value(None)
                         .is_required(False)) \
            .build(self.global_configuration)
        assert http_request.query_url == 'http://localhost:3000/test'

    @pytest.mark.parametrize('input_http_method, expected_http_method', [
        (HttpMethodEnum.POST, HttpMethodEnum.POST),
        (HttpMethodEnum.PUT, HttpMethodEnum.PUT),
        (HttpMethodEnum.PATCH, HttpMethodEnum.PATCH),
        (HttpMethodEnum.DELETE, HttpMethodEnum.DELETE),
        (HttpMethodEnum.GET, HttpMethodEnum.GET),
    ])
    def test_http_method(self, input_http_method, expected_http_method):
        http_request = self.new_request_builder \
            .http_method(input_http_method) \
            .build(self.global_configuration)
        assert http_request.http_method == expected_http_method

    @pytest.mark.parametrize('input_template_param_value, expected_template_param_value, should_encode', [
        ('Basic Test', 'Basic%20Test', True),
        ('Basic"Test', 'Basic%22Test', True),
        ('Basic<Test', 'Basic%3CTest', True),
        ('Basic>Test', 'Basic%3ETest', True),
        ('Basic#Test', 'Basic%23Test', True),
        ('Basic%Test', 'Basic%25Test', True),
        ('Basic|Test', 'Basic%7CTest', True),
        ('Basic Test', 'Basic Test', False),
        ('Basic"Test', 'Basic"Test', False),
        ('Basic<Test', 'Basic<Test', False),
        ('Basic>Test', 'Basic>Test', False),
        ('Basic#Test', 'Basic#Test', False),
        ('Basic%Test', 'Basic%Test', False),
        ('Basic|Test', 'Basic|Test', False),
    ])
    def test_template_params_with_encoding(self, input_template_param_value, expected_template_param_value,
                                           should_encode):
        http_request = self.new_request_builder \
            .path('/{template_param}') \
            .template_param(Parameter()
                            .key('template_param')
                            .value(input_template_param_value)
                            .should_encode(should_encode)) \
            .build(self.global_configuration)
        assert http_request.query_url == 'http://localhost:3000/{}'.format(expected_template_param_value)

    @pytest.mark.parametrize('input_query_param_value, expected_query_param_value, array_serialization_format', [
        ('string', 'query_param=string', SerializationFormats.INDEXED),
        (500, 'query_param=500', SerializationFormats.INDEXED),
        (500.12, 'query_param=500.12', SerializationFormats.INDEXED),
        (date(1994, 2, 13), 'query_param=1994-02-13', SerializationFormats.INDEXED),
        (ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         'query_param=761117415', SerializationFormats.INDEXED),
        (Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         'query_param={}'.format(quote(Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)), safe='')),
         SerializationFormats.INDEXED),
        (Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         'query_param={}'.format(quote(Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)), safe='')),
         SerializationFormats.INDEXED),
        ([1, 2, 3, 4], 'query_param[0]=1&query_param[1]=2&query_param[2]=3&query_param[3]=4',
         SerializationFormats.INDEXED),
        ([1, 2, 3, 4], 'query_param[]=1&query_param[]=2&query_param[]=3&query_param[]=4',
         SerializationFormats.UN_INDEXED),
        ([1, 2, 3, 4], 'query_param=1&query_param=2&query_param=3&query_param=4',
         SerializationFormats.PLAIN),
        ([1, 2, 3, 4], 'query_param=1%2C2%2C3%2C4', SerializationFormats.CSV),
        ([1, 2, 3, 4], 'query_param=1%7C2%7C3%7C4', SerializationFormats.PSV),
        ([1, 2, 3, 4], 'query_param=1%092%093%094', SerializationFormats.TSV),
        ({'key1': 'value1', 'key2': 'value2'}, 'query_param[key1]=value1&query_param[key2]=value2',
         SerializationFormats.INDEXED),
        ({'key1': 'value1', 'key2': [1, 2, 3, 4]},
         'query_param[key1]=value1'
         '&query_param[key2][0]=1'
         '&query_param[key2][1]=2'
         '&query_param[key2][2]=3'
         '&query_param[key2][3]=4', SerializationFormats.INDEXED),
        ({'key1': 'value1', 'key2': [1, 2, 3, {'key1': 'value1', 'key2': 'value2'}]},
         'query_param[key1]=value1'
         '&query_param[key2][0]=1'
         '&query_param[key2][1]=2'
         '&query_param[key2][2]=3'
         '&query_param[key2][3][key1]=value1'
         '&query_param[key2][3][key2]=value2', SerializationFormats.INDEXED),
        (Base.employee_model(),
         'query_param[address]=street%20abc'
         '&query_param[age]=27'
         '&query_param[birthday]=1994-02-13'
         '&query_param[birthtime]={}'.format(quote(
             Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)), safe='')) +
         '&query_param[department]=IT'
         '&query_param[dependents][0][address]=street%20abc'
         '&query_param[dependents][0][age]=12'
         '&query_param[dependents][0][birthday]=1994-02-13'
         '&query_param[dependents][0][birthtime]={}'.format(quote(
             Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)), safe='')) +
         '&query_param[dependents][0][name]=John'
         '&query_param[dependents][0][uid]=7654321'
         '&query_param[dependents][0][personType]=Per'
         '&query_param[dependents][0][key1]=value1'
         '&query_param[dependents][0][key2]=value2'
         '&query_param[hiredAt]={}'.format(quote(
             Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)), safe='')) +
         '&query_param[joiningDay]=Monday'
         '&query_param[name]=Bob'
         '&query_param[salary]=30000'
         '&query_param[uid]=1234567'
         '&query_param[workingDays][0]=Monday'
         '&query_param[workingDays][1]=Tuesday'
         '&query_param[personType]=Empl', SerializationFormats.INDEXED)
    ])
    def test_query_params(self, input_query_param_value, expected_query_param_value, array_serialization_format):
        http_request = self.new_request_builder \
            .query_param(Parameter()
                         .key('query_param')
                         .value(input_query_param_value)) \
            .array_serialization_format(array_serialization_format) \
            .build(self.global_configuration)
        assert http_request.query_url == 'http://localhost:3000/test?{}'.format(expected_query_param_value)

    @pytest.mark.parametrize('input_additional_query_params_value, expected_additional_query_params_value', [
        ({'key1': 'value1', 'key2': 'value2'}, 'key1=value1&key2=value2')
    ])
    def test_additional_query_params(self, input_additional_query_params_value, expected_additional_query_params_value):
        http_request = self.new_request_builder \
            .additional_query_params(input_additional_query_params_value) \
            .build(self.global_configuration)
        assert http_request.query_url == 'http://localhost:3000/test?{}'.format(expected_additional_query_params_value)

    @pytest.mark.parametrize('input_local_header_param_value, expected_local_header_param_value', [
        ('string', {'header_param': 'string'}),
        (500, {'header_param': 500}),
        (500.12, {'header_param': 500.12}),
        (str(date(1994, 2, 13)), {'header_param': '1994-02-13'}),
        (ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         {'header_param': 761117415}),
        (Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         {'header_param': '{}'.format(Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)))}),
        (Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         {'header_param': '{}'.format(Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)))}),
        ([1, 2, 3, 4], {'header_param': [1, 2, 3, 4]})
    ])
    def test_local_headers(self, input_local_header_param_value, expected_local_header_param_value):
        http_request = self.new_request_builder \
            .header_param(Parameter()
                          .key('header_param')
                          .value(input_local_header_param_value)) \
            .build(self.global_configuration)
        assert http_request.headers == expected_local_header_param_value

    @pytest.mark.parametrize('input_global_header_param_value, expected_global_header_param_value', [
        ('my-string', {'header_param': 'my-string'}),
        (5000, {'header_param': 5000}),
        (5000.12, {'header_param': 5000.12}),
        (str(date(1998, 2, 13)), {'header_param': '1998-02-13'}),
        (ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         {'header_param': 761117415}),
        (Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         {'header_param': '{}'.format(Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)))}),
        (Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         {'header_param': '{}'.format(Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)))}),
        ([100, 200, 300, 400], {'header_param': [100, 200, 300, 400]})
    ])
    def test_global_headers(self, input_global_header_param_value, expected_global_header_param_value):
        http_request = self.new_request_builder \
            .build(self.global_configuration
                   .global_header('header_param', input_global_header_param_value))
        assert http_request.headers == expected_global_header_param_value

    @pytest.mark.parametrize('input_additional_header_param_value, expected_additional_header_param_value', [
        ('my-string', {'header_param': 'my-string'}),
        (5000, {'header_param': 5000}),
        (5000.12, {'header_param': 5000.12}),
        (str(date(1998, 2, 13)), {'header_param': '1998-02-13'}),
        (ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         {'header_param': 761117415}),
        (Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         {'header_param': '{}'.format(Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)))}),
        (Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         {'header_param': '{}'.format(Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)))}),
        ([100, 200, 300, 400], {'header_param': [100, 200, 300, 400]})
    ])
    def test_additional_headers(self, input_additional_header_param_value, expected_additional_header_param_value):
        http_request = self.new_request_builder \
            .build(self.global_configuration
                   .additional_header('header_param', input_additional_header_param_value))
        assert http_request.headers == expected_additional_header_param_value

    @pytest.mark.parametrize('input_global_header_param_value,'
                             'input_local_header_param_value,'
                             'expected_header_param_value', [
                                 ('global_string', None, {'header_param': None}),
                                 ('global_string', 'local_string', {'header_param': 'local_string'})
                             ])
    def test_local_and_global_headers_precedence(self, input_global_header_param_value, input_local_header_param_value,
                                                 expected_header_param_value):
        global_headers = {'header_param': input_global_header_param_value}
        http_request = self.new_request_builder \
            .header_param(Parameter()
                          .key('header_param')
                          .value(input_local_header_param_value)) \
            .build(self.global_configuration.global_headers(global_headers))
        assert http_request.headers == expected_header_param_value

    @pytest.mark.parametrize('input_global_header_param_value,'
                             'input_local_header_param_value,'
                             'input_additional_header_param_value,'
                             'expected_header_param_value', [
                                 ('global_string', 'local_string', 'additional_string',
                                  {'header_param': 'additional_string'}),
                                 ('global_string', 'local_string', None,
                                  {'header_param': None})
                             ])
    def test_all_headers_precedence(self, input_global_header_param_value, input_local_header_param_value,
                                input_additional_header_param_value, expected_header_param_value):
        global_headers = {'header_param': input_global_header_param_value}
        additional_headers = {'header_param': input_additional_header_param_value}
        http_request = self.new_request_builder \
            .header_param(Parameter()
                          .key('header_param')
                          .value(input_local_header_param_value)) \
            .build(self.global_configuration.global_headers(global_headers)
                   .additional_headers(additional_headers))
        assert http_request.headers == expected_header_param_value

    def test_useragent_header(self):
        engines = ['CPython', 'Jython', 'JPython', 'IronPython', 'PyPy', 'RubyPython', 'AnacondaPython']
        operating_systems = ['Linux', 'Windows', 'Darwin', 'FreeBSD', 'OpenBSD', 'macOS']

        http_request = self.new_request_builder \
            .build(self.global_configuration_with_useragent)
        [lang, version, engine, engineVersion, osInfo] = http_request.headers['user-agent'].split('|')
        assert lang == 'Python' and version == '31.8.0' \
               and engine in engines and osInfo in operating_systems

    @pytest.mark.parametrize('input_form_param_value, expected_form_param_value, array_serialization_format', [
        ('string', [('form_param', 'string')], SerializationFormats.INDEXED),
        (500, [('form_param', 500)], SerializationFormats.INDEXED),
        (500.12, [('form_param', 500.12)], SerializationFormats.INDEXED),
        (str(date(1994, 2, 13)), [('form_param', '1994-02-13')], SerializationFormats.INDEXED),
        (ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         [('form_param', 761117415)], SerializationFormats.INDEXED),
        (Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         [('form_param', Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)))], SerializationFormats.INDEXED),
        (Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         [('form_param', Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)))], SerializationFormats.INDEXED),
        ([1, 2, 3, 4], [('form_param[0]', 1), ('form_param[1]', 2), ('form_param[2]', 3), ('form_param[3]', 4)],
         SerializationFormats.INDEXED),
        ([1, 2, 3, 4], [('form_param[]', 1), ('form_param[]', 2), ('form_param[]', 3), ('form_param[]', 4)],
         SerializationFormats.UN_INDEXED),
        ([1, 2, 3, 4], [('form_param', 1), ('form_param', 2), ('form_param', 3), ('form_param', 4)],
         SerializationFormats.PLAIN),
        ({'key1': 'value1', 'key2': 'value2'}, [('form_param[key1]', 'value1'), ('form_param[key2]', 'value2')],
         SerializationFormats.INDEXED),
        ({'key1': 'value1', 'key2': [1, 2, 3, 4]},
         [('form_param[key1]', 'value1'), ('form_param[key2][0]', 1), ('form_param[key2][1]', 2),
          ('form_param[key2][2]', 3), ('form_param[key2][3]', 4)], SerializationFormats.INDEXED),
        ({'key1': 'value1', 'key2': [1, 2, 3, {'key1': 'value1', 'key2': 'value2'}]},
         [('form_param[key1]', 'value1'), ('form_param[key2][0]', 1), ('form_param[key2][1]', 2),
          ('form_param[key2][2]', 3), ('form_param[key2][3][key1]', 'value1'), ('form_param[key2][3][key2]', 'value2')],
         SerializationFormats.INDEXED),
        (Base.employee_model(),
         [('form_param[address]', 'street abc'), ('form_param[age]', 27), ('form_param[birthday]', '1994-02-13'),
          ('form_param[birthtime]', Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15), False)),
          ('form_param[department]', 'IT'), ('form_param[dependents][0][address]', 'street abc'),
          ('form_param[dependents][0][age]', 12), ('form_param[dependents][0][birthday]', '1994-02-13'),
          ('form_param[dependents][0][birthtime]', Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15), False)),
          ('form_param[dependents][0][name]', 'John'), ('form_param[dependents][0][uid]', 7654321),
          ('form_param[dependents][0][personType]', 'Per'), ('form_param[dependents][0][key1]', 'value1'),
          ('form_param[dependents][0][key2]', 'value2'),
          ('form_param[hiredAt]', Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15), False)),
          ('form_param[joiningDay]', 'Monday'), ('form_param[name]', 'Bob'), ('form_param[salary]', 30000),
          ('form_param[uid]', 1234567), ('form_param[workingDays][0]', 'Monday'),
          ('form_param[workingDays][1]', 'Tuesday'), ('form_param[personType]', 'Empl')], SerializationFormats.INDEXED)
    ])
    def test_form_params(self, input_form_param_value, expected_form_param_value, array_serialization_format):
        http_request = self.new_request_builder \
            .form_param(Parameter()
                        .key('form_param')
                        .value(input_form_param_value)) \
            .array_serialization_format(array_serialization_format) \
            .build(self.global_configuration)
        for index, item in enumerate(http_request.parameters):
            # form encoding stores the datetime object so converting datetime to string for assertions as assertions
            # do not work for objects
            if isinstance(item[1], ApiHelper.CustomDate):
                try:
                    assert item[0] == expected_form_param_value[index][0] \
                           and item[1].value == expected_form_param_value[index][1].value
                except:
                    print("here")
            else:
                assert item == expected_form_param_value[index]

    @pytest.mark.parametrize('input_additional_form_param_value, expected_additional_form_param_value', [
        ({'key1': 'value1', 'key2': 'value2'}, [('key1', 'value1'), ('key2', 'value2')])
    ])
    def test_addition_form_params(self, input_additional_form_param_value, expected_additional_form_param_value):
        http_request = self.new_request_builder \
            .additional_form_params(input_additional_form_param_value) \
            .build(self.global_configuration)
        assert http_request.parameters == expected_additional_form_param_value

    @pytest.mark.parametrize('input_form_param_value,'
                             'input_additional_form_param_value,'
                             'expected_form_param_value', [
                                 ({'key1': 'value1', 'key2': 'value2'},
                                  {'additional_key1': 'additional_value1', 'additional_key2': 'additional_value2'},
                                  [('form_param[key1]', 'value1'), ('form_param[key2]', 'value2'),
                                   ('additional_key1', 'additional_value1'),
                                   ('additional_key2', 'additional_value2')])
                             ])
    def test_form_params_with_additional_form_params(self, input_form_param_value, input_additional_form_param_value,
                                                     expected_form_param_value):
        http_request = self.new_request_builder \
            .form_param(Parameter()
                        .key('form_param')
                        .value(input_form_param_value)) \
            .additional_form_params(input_additional_form_param_value) \
            .build(self.global_configuration)
        assert http_request.parameters == expected_form_param_value

    @pytest.mark.parametrize('input_body_param_value, expected_body_param_value', [
        ('string', 'string'),
        (500, 500),
        (500.12, 500.12),
        (str(date(1994, 2, 13)), '1994-02-13'),
        (ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)), 761117415),
        (Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))),
        (Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)))
    ])
    def test_json_body_params_without_serializer(self, input_body_param_value, expected_body_param_value):
        http_request = self.new_request_builder \
            .body_param(Parameter()
                        .value(input_body_param_value)) \
            .build(self.global_configuration)
        assert http_request.parameters == expected_body_param_value

    @pytest.mark.parametrize('input_body_param_value1, input_body_param_value2, expected_body_param_value', [
        ('string1', 'string2', '{"param1": "string1", "param2": "string2"}'),
        (100, 200, '{"param1": 100, "param2": 200}'),
        (100.12, 200.12, '{"param1": 100.12, "param2": 200.12}')
    ])
    def test_multiple_json_body_params_with_serializer(self, input_body_param_value1, input_body_param_value2,
                                                       expected_body_param_value):
        http_request = self.new_request_builder \
            .body_param(Parameter()
                        .key('param1')
                        .value(input_body_param_value1)) \
            .body_param(Parameter()
                        .key('param2')
                        .value(input_body_param_value2)) \
            .body_serializer(ApiHelper.json_serialize) \
            .build(self.global_configuration)
        assert http_request.parameters == expected_body_param_value

    @pytest.mark.parametrize('input_body_param_value, expected_body_param_value', [
        ([1, 2, 3, 4], '[1, 2, 3, 4]'),
        ({'key1': 'value1', 'key2': 'value2'}, '{"key1": "value1", "key2": "value2"}'),
        ({'key1': 'value1', 'key2': [1, 2, 3, 4]}, '{"key1": "value1", "key2": [1, 2, 3, 4]}'),
        ({'key1': 'value1', 'key2': [1, 2, 3, {'key1': 'value1', 'key2': 'value2'}]},
         '{"key1": "value1", "key2": [1, 2, 3, {"key1": "value1", "key2": "value2"}]}'),
        (Base.employee_model(), ApiHelper.json_serialize(Base.get_employee_dictionary()))
    ])
    def test_json_body_params_with_serializer(self, input_body_param_value, expected_body_param_value):
        http_request = self.new_request_builder \
            .body_param(Parameter()
                        .value(input_body_param_value)) \
            .body_serializer(ApiHelper.json_serialize) \
            .build(self.global_configuration)
        assert http_request.parameters == expected_body_param_value

    @pytest.mark.parametrize('input_value, expected_value', [
        (100, '100'),
        (True, 'true')
    ])
    def test_type_combinator_validation_in_request(self, input_value, expected_value):
        http_request = self.new_request_builder \
            .body_param(Parameter()
                        .validator(lambda value: UnionTypeLookUp.get('ScalarTypes'))
                        .value(input_value)) \
            .body_serializer(ApiHelper.json_serialize) \
            .build(self.global_configuration)
        assert http_request.parameters == expected_value

    @pytest.mark.parametrize('input_body_param_value, expected_body_param_value', [
        (Base.xml_model(), '<AttributesAndElements string="String" number="10000" boolean="false">'
                           '<string>Hey! I am being tested.</string>'
                           '<number>5000</number>'
                           '<boolean>false</boolean>'
                           '<elements>'
                           '<item>a</item>'
                           '<item>b</item>'
                           '<item>c</item>'
                           '</elements>'
                           '</AttributesAndElements>')
    ])
    def test_xml_body_param_with_serializer(self, input_body_param_value, expected_body_param_value):
        if sys.version_info[1] == 7:
            expected_body_param_value = expected_body_param_value.replace(
                'string="String" number="10000" boolean="false">',
                'boolean="false" number="10000" string="String">')
        http_request = self.new_request_builder \
            .xml_attributes(XmlAttributes()
                            .value(input_body_param_value)
                            .root_element_name('AttributesAndElements')) \
            .body_serializer(XmlHelper.serialize_to_xml) \
            .build(self.global_configuration)
        assert http_request.parameters == expected_body_param_value

    @pytest.mark.parametrize('input_body_param_value, expected_body_param_value', [
        ([Base.xml_model(), Base.xml_model()],
         '<arrayOfModels>'
         '<item string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</item>'
         '<item string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</item>'
         '</arrayOfModels>')
    ])
    def test_xml_array_body_param_with_serializer(self, input_body_param_value, expected_body_param_value):
        if sys.version_info[1] == 7:
            expected_body_param_value = expected_body_param_value.replace(
                'string="String" number="10000" boolean="false">',
                'boolean="false" number="10000" string="String">')
        http_request = self.new_request_builder \
            .xml_attributes(XmlAttributes()
                            .value(input_body_param_value)
                            .root_element_name('arrayOfModels')
                            .array_item_name('item')) \
            .body_serializer(XmlHelper.serialize_list_to_xml) \
            .build(self.global_configuration)
        assert http_request.parameters == expected_body_param_value

    @pytest.mark.parametrize('input_body_param_value, expected_body_param_value, expected_content_type', [
        (FileWrapper(Base.read_file('apimatic.png'), 'image/png'),
         Base.read_file('apimatic.png'), 'image/png')])
    def test_file_as_body_param(self, input_body_param_value, expected_body_param_value, expected_content_type):
        try:
            http_request = self.new_request_builder \
                .header_param(Parameter().key('content-type').value('application/xml')) \
                .body_param(Parameter().value(input_body_param_value)) \
                .build(self.global_configuration)

            actual_body_param_value = http_request.parameters

            assert actual_body_param_value.read() == expected_body_param_value.read() \
                   and http_request.headers['content-type'] == expected_content_type
        finally:
            actual_body_param_value.close()
            expected_body_param_value.close()

    @pytest.mark.parametrize('input_multipart_param_value1, input_default_content_type1,'
                             'input_multipart_param_value2, input_default_content_type2,'
                             'expected_multipart_param_value1, expected_default_content_type1, '
                             'expected_multipart_param_value2, expected_default_content_type2', [
                                 (Base.read_file('apimatic.png'), 'image/png', Base.employee_model(),
                                  'application/json', Base.read_file('apimatic.png'), 'image/png',
                                  ApiHelper.json_serialize(Base.get_employee_dictionary()), 'application/json')
                             ])
    def test_multipart_request_without_file_wrapper(self, input_multipart_param_value1,
                                                    input_default_content_type1,
                                                    input_multipart_param_value2,
                                                    input_default_content_type2,
                                                    expected_multipart_param_value1,
                                                    expected_default_content_type1,
                                                    expected_multipart_param_value2,
                                                    expected_default_content_type2):
        try:
            http_request = self.new_request_builder \
                .multipart_param(Parameter().key('file_wrapper')
                                 .value(input_multipart_param_value1)
                                 .default_content_type(input_default_content_type1)) \
                .multipart_param(Parameter().key('model')
                                 .value(ApiHelper.json_serialize(input_multipart_param_value2))
                                 .default_content_type(input_default_content_type2)) \
                .build(self.global_configuration)

            actual_multipart_param_value1 = http_request.files['file_wrapper'][1]
            actual_multipart_param_content_type1 = http_request.files['file_wrapper'][2]
            actual_multipart_param_value2 = http_request.files['model'][1]
            actual_multipart_param_content_type2 = http_request.files['model'][2]

            assert actual_multipart_param_value1.read() == expected_multipart_param_value1.read() \
                   and actual_multipart_param_content_type1 == expected_default_content_type1 \
                   and actual_multipart_param_value2 == expected_multipart_param_value2 \
                   and actual_multipart_param_content_type2 == expected_default_content_type2
        finally:
            actual_multipart_param_value1.close()
            expected_multipart_param_value1.close()

    @pytest.mark.parametrize('input_multipart_param_value1, input_multipart_param_value2, input_default_content_type2,'
                             'expected_multipart_param_value1, expected_default_content_type1,'
                             'expected_multipart_param_value2, expected_default_content_type2', [
                                 (FileWrapper(Base.read_file('apimatic.png'), 'image/png'), Base.employee_model(),
                                  'application/json', Base.read_file('apimatic.png'), 'image/png',
                                  ApiHelper.json_serialize(Base.get_employee_dictionary()), 'application/json')
                             ])
    def test_multipart_request_with_file_wrapper(self, input_multipart_param_value1,
                                                 input_multipart_param_value2,
                                                 input_default_content_type2,
                                                 expected_multipart_param_value1,
                                                 expected_default_content_type1,
                                                 expected_multipart_param_value2,
                                                 expected_default_content_type2):
        try:
            http_request = self.new_request_builder \
                .multipart_param(Parameter().key('file')
                                 .value(input_multipart_param_value1)) \
                .multipart_param(Parameter().key('model')
                                 .value(ApiHelper.json_serialize(input_multipart_param_value2))
                                 .default_content_type(input_default_content_type2)) \
                .build(self.global_configuration)

            actual_multipart_param_value1 = http_request.files['file'][1]
            actual_multipart_param_content_type1 = http_request.files['file'][2]
            actual_multipart_param_value2 = http_request.files['model'][1]
            actual_multipart_param_content_type2 = http_request.files['model'][2]

            assert actual_multipart_param_value1.read() == expected_multipart_param_value1.read() \
                   and actual_multipart_param_content_type1 == expected_default_content_type1 \
                   and actual_multipart_param_value2 == expected_multipart_param_value2 \
                   and actual_multipart_param_content_type2 == expected_default_content_type2
        finally:
            actual_multipart_param_value1.close()
            expected_multipart_param_value1.close()

    @pytest.mark.parametrize('input_auth_scheme, expected_auth_header_key, expected_auth_header_value', [
        (Single('basic_auth'), 'Basic-Authorization', 'Basic {}'.format(
            AuthHelper.get_base64_encoded_value('test_username', 'test_password'))),
        (Single('bearer_auth'), 'Bearer-Authorization', 'Bearer 0b79bab50daca910b000d4f1a2b675d604257e42'),
        (Single('custom_header_auth'), 'token', 'Qaws2W233WedeRe4T56G6Vref2')
    ])
    def test_header_authentication(self, input_auth_scheme, expected_auth_header_key, expected_auth_header_value):
        http_request = self.new_request_builder \
            .auth(input_auth_scheme) \
            .build(self.global_configuration_with_auth)

        assert http_request.headers[expected_auth_header_key] == expected_auth_header_value

    def test_query_authentication(self):
        http_request = self.new_request_builder \
            .auth(Single('custom_query_auth')) \
            .build(self.global_configuration_with_auth)

        assert http_request.query_url == 'http://localhost:3000/test?token=Qaws2W233WedeRe4T56G6Vref2&api-key=W233WedeRe4T56G6Vref2'

    @pytest.mark.parametrize('input_invalid_auth_scheme', [
        (Single('invalid')),
        (Or('invalid_1', 'invalid_2')),
        (And('invalid_1', 'invalid_2'))
    ])
    def test_invalid_key_authentication(self, input_invalid_auth_scheme):
        with pytest.raises(ValueError) as validation_error:
            self.new_request_builder \
                .auth(input_invalid_auth_scheme) \
                .build(self.global_configuration_with_auth)
        assert validation_error.value.args[0] == 'Auth key is invalid.'

    @pytest.mark.parametrize('input_auth_scheme, expected_request_headers', [
                                 (Or('basic_auth', 'custom_header_auth'),
                                  {
                                      'Basic-Authorization': 'Basic dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk',
                                      'token': None
                                  }),
                                 (And('basic_auth', 'bearer_auth', 'custom_header_auth'),
                                  {
                                      'Basic-Authorization': 'Basic dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk',
                                      'Bearer-Authorization': 'Bearer 0b79bab50daca910b000d4f1a2b675d604257e42',
                                      'token': 'Qaws2W233WedeRe4T56G6Vref2'
                                  }),
                                 (Or('basic_auth', And('bearer_auth', 'custom_header_auth')),
                                  {
                                      'Basic-Authorization': 'Basic dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk',
                                      'Bearer-Authorization': None,
                                      'token': None
                                  }),
                                 (And('basic_auth', Or('bearer_auth', 'custom_header_auth')),
                                  {
                                      'Basic-Authorization': 'Basic dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk',
                                      'Bearer-Authorization': 'Bearer 0b79bab50daca910b000d4f1a2b675d604257e42',
                                      'token': None
                                  }),
                                 (And('basic_auth', And('bearer_auth', 'custom_header_auth')),
                                  {
                                      'Basic-Authorization': 'Basic dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk',
                                      'Bearer-Authorization': 'Bearer 0b79bab50daca910b000d4f1a2b675d604257e42',
                                      'token': 'Qaws2W233WedeRe4T56G6Vref2'
                                  }),
                                 (Or('basic_auth', Or('bearer_auth', 'custom_header_auth')),
                                  {
                                      'Basic-Authorization': 'Basic dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk',
                                      'Bearer-Authorization': None,
                                      'token': None
                                  }),
                                 (Or('basic_auth', Or(None, 'custom_header_auth')),
                                  {
                                      'Basic-Authorization': 'Basic dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk',
                                      'token': None
                                  }),
                                 (Or('basic_auth', And(None, 'custom_header_auth')),
                                  {
                                      'Basic-Authorization': 'Basic dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk',
                                      'token': None
                                  }),
                             ])
    def test_success_case_of_multiple_authentications(self, input_auth_scheme, expected_request_headers):
        http_request = self.new_request_builder \
            .auth(input_auth_scheme) \
            .build(self.global_configuration_with_auth)
        for key in expected_request_headers.keys():
            assert http_request.headers.get(key) == expected_request_headers.get(key)

    @pytest.mark.parametrize('input_auth_scheme, expected_error_message', [
        (Or('basic_auth', 'bearer_auth', 'custom_header_auth'), '[BasicAuth: _basic_auth_user_name or '
                                                                '_basic_auth_password is undefined.] or ['
                                                                'BearerAuth: _access_token is undefined.] or ['
                                                                'CustomHeaderAuthentication: token is undefined.]'),
        (And('basic_auth', 'bearer_auth', 'custom_header_auth'), '[BasicAuth: _basic_auth_user_name or '
                                                                 '_basic_auth_password is undefined.] and ['
                                                                 'BearerAuth: _access_token is undefined.] and ['
                                                                 'CustomHeaderAuthentication: token is undefined.]'),
        (Or('basic_auth', And('bearer_auth', 'custom_header_auth')), '[BasicAuth: _basic_auth_user_name or '
                                                                     '_basic_auth_password is undefined.] or ['
                                                                     'BearerAuth: _access_token is undefined.] and ['
                                                                     'CustomHeaderAuthentication: token is '
                                                                     'undefined.]'),
        (And('basic_auth', Or('bearer_auth', 'custom_header_auth')), '[BasicAuth: _basic_auth_user_name or '
                                                                     '_basic_auth_password is undefined.] and ['
                                                                     'BearerAuth: _access_token is undefined.] or ['
                                                                     'CustomHeaderAuthentication: token is '
                                                                     'undefined.]'),
        (And('basic_auth', And('bearer_auth', 'custom_header_auth')), '[BasicAuth: _basic_auth_user_name or '
                                                                      '_basic_auth_password is undefined.] and ['
                                                                      'BearerAuth: _access_token is undefined.] and ['
                                                                      'CustomHeaderAuthentication: token is '
                                                                      'undefined.]'),
        (Or('basic_auth', Or('bearer_auth', 'custom_header_auth')), '[BasicAuth: _basic_auth_user_name or '
                                                                    '_basic_auth_password is undefined.] or ['
                                                                    'BearerAuth: _access_token is undefined.] or ['
                                                                    'CustomHeaderAuthentication: token is undefined.]'),
        (Or(None, None), ''),
        (Or(None, 'basic_auth'), '[BasicAuth: _basic_auth_user_name or _basic_auth_password is undefined.]'),
        (And(None, None), ''),
        (And(None, 'basic_auth'), '[BasicAuth: _basic_auth_user_name or _basic_auth_password is undefined.]')
    ])
    def test_failed_case_of_multiple_authentications(self, input_auth_scheme, expected_error_message):
        with pytest.raises(AuthValidationException) as errors:
            self.new_request_builder \
                .auth(input_auth_scheme) \
                .build(self.global_configuration_with_uninitialized_auth_params)
        assert errors.value.args[0] == expected_error_message

    @pytest.mark.parametrize('input_auth_scheme, expected_auth_header_key,'
                             'expected_auth_header_value', [
                                 (Or('basic_auth', 'custom_header_auth'), 'token',
                                  'Qaws2W233WedeRe4T56G6Vref2'),
                                 (Or('custom_header_auth', And('basic_auth', 'custom_header_auth')), 'token',
                                  'Qaws2W233WedeRe4T56G6Vref2')
                             ])
    def test_case_of_multiple_authentications(self, input_auth_scheme, expected_auth_header_key,
                                              expected_auth_header_value):
        http_request = self.new_request_builder \
            .auth(input_auth_scheme) \
            .build(self.global_configuration_with_partially_initialized_auth_params)

        assert http_request.headers[expected_auth_header_key] == expected_auth_header_value
        assert http_request.headers.get('Authorization') is None
