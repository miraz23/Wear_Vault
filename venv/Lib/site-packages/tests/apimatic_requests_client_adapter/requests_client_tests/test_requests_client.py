import pytest
from apimatic_core_interfaces.types.http_method_enum import HttpMethodEnum

from tests.apimatic_requests_client_adapter.base import Base


class TestRequestsClient(Base):

    @pytest.mark.parametrize('http_response, contains_binary_response, http_request, expected_response', [
        (Base.actual_response_from_client(content='binary content'), True, Base.request(),
         Base.response(text='binary content')),
        (Base.actual_response_from_client(text='simple content'), False, Base.request(),
         Base.response(text='simple content'))
    ])
    def test_convert_response(self, http_response, contains_binary_response, http_request, expected_response):
        actual_response = self.client.convert_response(http_response, contains_binary_response, http_request)
        assert actual_response.status_code == expected_response.status_code \
               and actual_response.reason_phrase == expected_response.reason_phrase \
               and actual_response.headers == expected_response.headers \
               and actual_response.text == expected_response.text \
               and actual_response.request.http_method == expected_response.request.http_method \
               and actual_response.request.query_url == expected_response.request.query_url \
               and actual_response.request.headers == expected_response.request.headers \
               and actual_response.request.query_parameters == expected_response.request.query_parameters \
               and actual_response.request.parameters == expected_response.request.parameters \
               and actual_response.request.files == expected_response.request.files

    @pytest.mark.parametrize('timeout, cache, max_retries, backoff_factor, retry_statuses, '
                             'retry_methods, verify, http_client_instance, override_http_client_configuration, '
                             'expected_timeout, expected_max_retries, expected_backoff_factor, '
                             'expected_retry_statuses, expected_retry_methods, expected_verify, '
                             'expected_raise_on_status, expected_raise_on_redirect',
                             [
                                 (100, False, 10, 4.3, [400, 401, 415, 429], [HttpMethodEnum.GET], False, None, False,
                                  100, 10, 4.3, [400, 401, 415, 429], [HttpMethodEnum.GET], False, False, False),
                                 (100, True, 10, 4.3, [400, 401, 415, 429], [HttpMethodEnum.GET], False, None, False,
                                  100, 10, 4.3, [400, 401, 415, 429], [HttpMethodEnum.GET], False, False, False),
                                 (100, False, 10, 4.3, [400, 401, 415, 429], [HttpMethodEnum.GET], False,
                                  Base.custom_requests_client(500, False, 1000, 55.5, [400],
                                                              [HttpMethodEnum.DELETE], True, None,
                                                              False), False,
                                  500, 1000, 55.5, [400], [HttpMethodEnum.DELETE], True, False, False),
                                 (100, False, 10, 4.3, [400, 401, 415, 429], [HttpMethodEnum.GET], False,
                                  Base.custom_requests_client(500, False, 1000, 55.5, [400],
                                                              [HttpMethodEnum.DELETE], True, None,
                                                              False), True,
                                  100, 10, 4.3, [400, 401, 415, 429], [HttpMethodEnum.GET], False, False, False)
                             ])
    def test_custom_client(self, timeout, cache, max_retries, backoff_factor, retry_statuses,
                           retry_methods, verify, http_client_instance, override_http_client_configuration,
                           expected_timeout, expected_max_retries, expected_backoff_factor, expected_retry_statuses,
                           expected_retry_methods, expected_verify, expected_raise_on_status,
                           expected_raise_on_redirect):
        actual_client = Base.custom_requests_client(timeout, cache, max_retries, backoff_factor, retry_statuses,
                                                    retry_methods, verify, http_client_instance,
                                                    override_http_client_configuration)
        for adapter in actual_client.session.adapters.values():
            assert adapter.max_retries.total == expected_max_retries
            assert adapter.max_retries.backoff_factor == expected_backoff_factor
            assert adapter.max_retries.status_forcelist == expected_retry_statuses
            assert adapter.max_retries.allowed_methods == expected_retry_methods
            assert adapter.max_retries.raise_on_status == expected_raise_on_status
            assert adapter.max_retries.raise_on_redirect == expected_raise_on_redirect

        assert actual_client.timeout == expected_timeout \
               and actual_client.session.verify == expected_verify

    def test_default_force_retries(self):
        actual_client = self.custom_requests_client(max_retries=10,
                                                    retry_methods=[HttpMethodEnum.GET, HttpMethodEnum.DELETE])
        actual_client.force_retries(self.request())
        for adapter in actual_client.session.adapters.values():
            assert adapter.max_retries.total == 10
            assert adapter.max_retries.allowed_methods == [HttpMethodEnum.GET, HttpMethodEnum.DELETE]

    def test_disabled_force_retries(self):
        actual_client = self.client
        actual_client.force_retries(self.request(), should_retry=False)
        for adapter in actual_client.session.adapters.values():
            assert adapter.max_retries == False

    def test_enabled_force_retries(self):
        actual_client = self.client
        request = self.request()
        actual_client.force_retries(request, should_retry=True)
        for adapter in actual_client.session.adapters.values():
            assert adapter.max_retries.allowed_methods == [request.http_method]


