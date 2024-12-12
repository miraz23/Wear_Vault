from datetime import datetime, date
import pytest
import sys
from apimatic_core.types.datetime_format import DateTimeFormat
from apimatic_core.utilities.api_helper import ApiHelper
from apimatic_core.utilities.xml_helper import XmlHelper
from tests.apimatic_core.base import Base
from tests.apimatic_core.mocks.exceptions.api_exception import APIException
from tests.apimatic_core.mocks.exceptions.global_test_exception import GlobalTestException
from tests.apimatic_core.mocks.exceptions.local_test_exception import LocalTestException
from tests.apimatic_core.mocks.exceptions.nested_model_exception import NestedModelException
from tests.apimatic_core.mocks.models.api_response import ApiResponse
from tests.apimatic_core.mocks.models.person import Employee
from tests.apimatic_core.mocks.models.xml_model import XMLModel


class TestResponseHandler(Base):

    def test_nullify_404(self):
        http_response = self.new_response_handler.is_nullify404(True).handle(self.response(status_code=404),
                                                                             self.global_errors())
        assert http_response is None

    @pytest.mark.parametrize('http_response, expected_exception_type, expected_error_message', [
        (Base.response(status_code=400), GlobalTestException, '400 Global'),
        (Base.response(status_code=412), NestedModelException, 'Precondition Failed'),
        (Base.response(status_code=429), GlobalTestException, 'Invalid response'),
        (Base.response(status_code=399), GlobalTestException, '3XX Global')
    ])
    def test_global_error(self, http_response, expected_exception_type, expected_error_message):
        with pytest.raises(expected_exception_type) as error:
            self.new_response_handler.handle(http_response, self.global_errors())
        assert error.value.reason == expected_error_message

    def test_local_error(self):
        with pytest.raises(LocalTestException) as error:
            self.new_response_handler.local_error(404, 'Not Found', LocalTestException) \
                .handle(self.response(status_code=404), self.global_errors())
        assert error.value.reason == 'Not Found'

    def test_default_local_error(self):
        with pytest.raises(LocalTestException) as error:
            self.new_response_handler.local_error(404, 'Not Found', LocalTestException) \
                .local_error('default', 'Response Not OK', LocalTestException) \
                .handle(self.response(status_code=412), self.global_errors())
        assert error.value.reason == 'Response Not OK'

    @pytest.mark.parametrize('http_response, expected_exception_type, expected_error_message', [
        (Base.response(status_code=501), APIException, '5XX local'),
        (Base.response(status_code=443), LocalTestException, '4XX local'),
        (Base.response(status_code=522), LocalTestException, '522 local')
    ])
    def test_default_range_local_error(self, http_response, expected_exception_type, expected_error_message):
        with pytest.raises(expected_exception_type) as error:
            self.new_response_handler.local_error(522, '522 local', LocalTestException) \
                .local_error('5XX', '5XX local', APIException) \
                .local_error('4XX', '4XX local', LocalTestException) \
                .handle(http_response, self.global_errors())
        assert error.value.reason == expected_error_message

    def test_local_error_with_body(self):
        with pytest.raises(LocalTestException) as error:
            self.new_response_handler.local_error(404, 'Not Found', LocalTestException) \
                .handle(self.response(status_code=404,
                                      text='{"ServerCode": 5001, '
                                           '"ServerMessage": "Test message from server", '
                                           '"SecretMessageForEndpoint": "This is test error message"}'),
                        self.global_errors())
        assert error.value.server_code == 5001 \
               and error.value.server_message == 'Test message from server' \
               and error.value.secret_message_for_endpoint == 'This is test error message'

    def test_local_error_template_message(self):
        with pytest.raises(LocalTestException) as error:
            self.new_response_handler.local_error_template(404, 'error_code => {$statusCode}, '
                                                                'header => {$response.header.accept}, '
                                                                'body => {$response.body#/ServerCode} - '
                                                                '{$response.body#/ServerMessage} - '
                                                                '{$response.body#/SecretMessageForEndpoint}',
                                                           LocalTestException) \
                .handle(self.response(status_code=404, text='{"ServerCode": 5001, "ServerMessage": '
                                                            '"Test message from server", "SecretMessageForEndpoint": '
                                                            '"This is test error message"}',
                                      headers={'accept': 'application/json'}),
                        self.global_errors_with_template_message())
        assert error.value.reason == 'error_code => 404, ' \
                                     'header => application/json, ' \
                                     'body => 5001 - Test message from server - This is test error message'

    def test_global_error_with_body(self):
        with pytest.raises(NestedModelException) as error:
            self.new_response_handler.local_error(404, 'Not Found', LocalTestException) \
                .handle(self.response(status_code=412,
                                      text='{"ServerCode": 5001, '
                                           '"ServerMessage": "Test message from server", '
                                           '"model": { '
                                           '"field": "Test field", '
                                           '"name": "Test name", '
                                           '"address": "Test address"'
                                           '}'
                                           '}'),
                        self.global_errors())
        assert error.value.server_code == 5001 \
               and error.value.server_message == 'Test message from server' \
               and error.value.model.field == 'Test field' \
               and error.value.model.name == 'Test name' \
               and error.value.model.address == 'Test address'

    def test_global_error_template_message(self):
        with pytest.raises(NestedModelException) as error:
            self.new_response_handler.local_error(404, 'Not Found', LocalTestException) \
                .handle(self.response(status_code=412,
                                      text='{"ServerCode": 5001, "ServerMessage": "Test message from server", "model": '
                                           '{ "field": "Test field", "name": "Test name", "address": "Test address"}}'),
                        self.global_errors_with_template_message())

        assert error.value.reason == 'global error message -> error_code => 412, header => ,' \
                                     ' body => 5001 - Test message from server - Test name'

    def test_local_error_precedence(self):
        with pytest.raises(LocalTestException) as error:
            self.new_response_handler.local_error(400, '400 Local', LocalTestException) \
                .handle(self.response(status_code=400), self.global_errors())
        assert error.value.reason == '400 Local'

    def test_global_error_precedence(self):
        with pytest.raises(GlobalTestException) as error:
            self.new_response_handler.local_error(404, 'Not Found', LocalTestException) \
                .handle(self.response(status_code=400), self.global_errors())
        assert error.value.reason == '400 Global'

    @pytest.mark.parametrize('input_http_response, expected_response_body', [
        (Base.response(text='This is a string response'), 'This is a string response'),
        (Base.response(text=500), 500),
        (Base.response(text=500.124), 500.124)
    ])
    def test_simple_response_body(self, input_http_response, expected_response_body):
        http_response = self.new_response_handler.handle(input_http_response, self.global_errors())
        assert http_response == expected_response_body

    @pytest.mark.parametrize('input_http_response, input_response_convertor, expected_response_body_type, '
                             'expected_response_body', [
                                 (Base.response(text='500'), int, int, 500),
                                 (Base.response(text=500), str, str, '500')
                             ])
    def test_simple_response_body_with_convertor(self, input_http_response, input_response_convertor,
                                                 expected_response_body_type, expected_response_body):
        http_response = self.new_response_handler.convertor(input_response_convertor).handle(input_http_response,
                                                                                             self.global_errors())
        assert type(http_response) == expected_response_body_type and http_response == expected_response_body

    @pytest.mark.parametrize('input_http_response, expected_response_body', [
        (Base.response(text=ApiHelper.json_serialize(Base.employee_model())),
         ApiHelper.json_serialize(Base.employee_model())),
        (Base.response(), None),
        (Base.response(text=''), None),
        (Base.response(text='    '), None)
    ])
    def test_custom_type_response_body(self, input_http_response, expected_response_body):
        http_response = self.new_response_handler \
            .deserializer(ApiHelper.json_deserialize) \
            .deserialize_into(Employee.from_dictionary) \
            .handle(input_http_response, self.global_errors())
        assert ApiHelper.json_serialize(http_response) == expected_response_body

    @pytest.mark.parametrize('input_http_response, expected_response_body', [
        (Base.response(text='[1, 2, 3, 4]'), '[1, 2, 3, 4]'),
        (Base.response(text='{"key1": "value1", "key2": "value2"}'), '{"key1": "value1", "key2": "value2"}'),
        (Base.response(text='{"key1": "value1", "key2": [1, 2, 3, {"key1": "value1", "key2": "value2"}]}'),
         '{"key1": "value1", "key2": [1, 2, 3, {"key1": "value1", "key2": "value2"}]}'),
        (Base.response(), None),
        (Base.response(text=''), None),
        (Base.response(text='    '), None)
    ])
    def test_json_response_body(self, input_http_response, expected_response_body):
        http_response = self.new_response_handler \
            .deserializer(ApiHelper.json_deserialize) \
            .handle(input_http_response, self.global_errors())
        assert ApiHelper.json_serialize(http_response) == expected_response_body

    @pytest.mark.parametrize('input_http_response, expected_response_body', [
        (Base.response(text=XmlHelper.serialize_list_to_xml(
            [Base.xml_model(), Base.xml_model()], 'arrayOfModels', 'item')),
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
         '</arrayOfModels>'),
    ])
    def test_xml_response_body_with_item_name(self, input_http_response, expected_response_body):
        if sys.version_info[1] == 7:
            expected_response_body = expected_response_body.replace('string="String" number="10000" boolean="false">',
                                                                    'boolean="false" number="10000" string="String">')
        http_response = self.new_response_handler \
            .is_xml_response(True) \
            .deserializer(XmlHelper.deserialize_xml_to_list) \
            .deserialize_into(XMLModel) \
            .xml_item_name('item') \
            .handle(input_http_response, self.global_errors())
        assert XmlHelper.serialize_list_to_xml(http_response, 'arrayOfModels', 'item') == expected_response_body

    @pytest.mark.parametrize('input_http_response, expected_response_body', [
        (Base.response(text=XmlHelper.serialize_to_xml(Base.xml_model(), 'AttributesAndElements')),
         '<AttributesAndElements string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</AttributesAndElements>'),
    ])
    def test_xml_response_body_without_item_name(self, input_http_response, expected_response_body):
        if sys.version_info[1] == 7:
            expected_response_body = expected_response_body.replace('string="String" number="10000" boolean="false">',
                                                                    'boolean="false" number="10000" string="String">')
        http_response = self.new_response_handler \
            .is_xml_response(True) \
            .deserializer(XmlHelper.deserialize_xml) \
            .deserialize_into(XMLModel) \
            .handle(input_http_response, self.global_errors())
        assert XmlHelper.serialize_to_xml(http_response, 'AttributesAndElements') == expected_response_body

    @pytest.mark.parametrize('input_http_response, expected_response_body', [
        (Base.response(text='[1, 2, 3, 4]'), '[1, 2, 3, 4]'),
        (Base.response(text='{"key1": "value1", "key2": "value2"}'), '{"key1": "value1", "key2": "value2"}'),
        (Base.response(text='{"key1": "value1", "key2": [1, 2, 3, {"key1": "value1", "key2": "value2"}]}'),
         '{"key1": "value1", "key2": [1, 2, 3, {"key1": "value1", "key2": "value2"}]}')
    ])
    def test_api_response(self, input_http_response, expected_response_body):
        api_response = self.new_response_handler \
            .deserializer(ApiHelper.json_deserialize) \
            .is_api_response(True) \
            .handle(input_http_response, self.global_errors())
        assert ApiHelper.json_serialize(api_response.body) == expected_response_body
        assert api_response.is_success() is True
        assert api_response.is_error() is False
        assert str(api_response) == '<CoreApiResponse {}>'.format(expected_response_body)

    @pytest.mark.parametrize('input_http_response, expected_response_body, expected_error_list', [
        (Base.response(text='{"key1": "value1", "key2": "value2", "errors": ["e1", "e2"], "cursor": "Test cursor"}'),
         '{"key1": "value1", "key2": "value2", "errors": ["e1", "e2"], "cursor": "Test cursor"}', ['e1', 'e2'])
    ])
    def test_api_response_convertor(self, input_http_response, expected_response_body, expected_error_list):
        api_response = self.new_response_handler \
            .deserializer(ApiHelper.json_deserialize) \
            .is_api_response(True) \
            .convertor(ApiResponse.create) \
            .handle(input_http_response, self.global_errors())
        assert isinstance(api_response, ApiResponse) and \
               ApiHelper.json_serialize(api_response.body) == expected_response_body \
               and api_response.errors == expected_error_list \
               and api_response.cursor == "Test cursor"

    @pytest.mark.parametrize('input_http_response, expected_response_body, expected_error_list', [
        (Base.response(text='{"key1": "value1", "key2": "value2", "errors": ["e1", "e2"]}'),
         '{"key1": "value1", "key2": "value2", "errors": ["e1", "e2"]}', ['e1', 'e2']),
        (Base.response(text=''), None, None),
        (Base.response(text='    '), None, None)
    ])
    def test_api_response_with_errors(self, input_http_response, expected_response_body, expected_error_list):
        api_response = self.new_response_handler \
            .deserializer(ApiHelper.json_deserialize) \
            .is_api_response(True) \
            .handle(input_http_response, self.global_errors())
        assert ApiHelper.json_serialize(api_response.body) == expected_response_body \
               and api_response.errors == expected_error_list

    @pytest.mark.parametrize('input_http_response, input_date_time_format, expected_response_body', [
        (Base.response(text=ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))),
         DateTimeFormat.UNIX_DATE_TIME, datetime(1994, 2, 13, 5, 30, 15)),
        (Base.response(text=ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))),
         DateTimeFormat.HTTP_DATE_TIME, datetime(1994, 2, 13, 5, 30, 15)),
        (Base.response(text=ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))),
         DateTimeFormat.RFC3339_DATE_TIME, datetime(1994, 2, 13, 5, 30, 15)),

        (Base.response(
            text=ApiHelper.json_serialize([ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
                                           ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))])),
         DateTimeFormat.UNIX_DATE_TIME, [datetime(1994, 2, 13, 5, 30, 15), datetime(1994, 2, 13, 5, 30, 15)]),

        (Base.response(
            text=ApiHelper.json_serialize([ApiHelper.HttpDateTime.from_datetime(datetime(1995, 2, 13, 5, 30, 15)),
                                           ApiHelper.HttpDateTime.from_datetime(datetime(1995, 2, 13, 5, 30, 15))])),
         DateTimeFormat.HTTP_DATE_TIME, [datetime(1995, 2, 13, 5, 30, 15), datetime(1995, 2, 13, 5, 30, 15)]),

        (Base.response(
            text=ApiHelper.json_serialize([ApiHelper.RFC3339DateTime.from_datetime(datetime(1996, 2, 13, 5, 30, 15)),
                                           ApiHelper.RFC3339DateTime.from_datetime(datetime(1996, 2, 13, 5, 30, 15))])),
         DateTimeFormat.RFC3339_DATE_TIME, [datetime(1996, 2, 13, 5, 30, 15), datetime(1996, 2, 13, 5, 30, 15)])

    ])
    def test_date_time_response_body(self, input_http_response, input_date_time_format, expected_response_body):
        http_response = self.new_response_handler \
            .deserializer(ApiHelper.datetime_deserialize) \
            .datetime_format(input_date_time_format) \
            .handle(input_http_response, self.global_errors())
        assert http_response == expected_response_body

    @pytest.mark.parametrize('input_http_response, expected_response_body', [
        (Base.response(text=str(date(1994, 2, 13))), date(1994, 2, 13)),
        (Base.response(text=ApiHelper.json_serialize([str(date(1994, 2, 13)), str(date(1994, 2, 13))])),
         [date(1994, 2, 13), date(1994, 2, 13)])
    ])
    def test_date_response_body(self, input_http_response, expected_response_body):
        http_response = self.new_response_handler \
            .deserializer(ApiHelper.date_deserialize) \
            .handle(input_http_response, self.global_errors())
        assert http_response == expected_response_body
