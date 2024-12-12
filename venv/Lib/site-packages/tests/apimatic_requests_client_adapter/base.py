from apimatic_core_interfaces.types.http_method_enum import HttpMethodEnum
from apimatic_requests_client_adapter.requests_client import RequestsClient
from tests.apimatic_requests_client_adapter.models.internal.http_request import HttpRequest
from tests.apimatic_requests_client_adapter.models.internal.http_response import HttpResponse
from tests.apimatic_requests_client_adapter.models.external.http_response import HttpResponse as ActualHttpResponse
from tests.apimatic_requests_client_adapter.models.internal.http_response_factory import HttpResponseFactory


class Base:

    @staticmethod
    def request():
        return HttpRequest(http_method=HttpMethodEnum.GET, query_url='http://localhost:3000/test')

    @staticmethod
    def response(status_code=200, reason_phrase=None, headers=None, text=None):
        return HttpResponse(status_code=status_code, reason_phrase=reason_phrase,
                            headers=headers, text=text, request=Base.request())

    @staticmethod
    def actual_response_from_client(status_code=200, reason=None, headers=None, text=None, content=None):
        return ActualHttpResponse(status_code=status_code, reason=reason, headers=headers, text=text, content=content)

    @property
    def client(self):
        return RequestsClient(response_factory=HttpResponseFactory())

    @staticmethod
    def custom_requests_client(timeout=60,
                               cache=False,
                               max_retries=None,
                               backoff_factor=None,
                               retry_statuses=None,
                               retry_methods=None,
                               verify=True,
                               http_client_instance=None,
                               override_http_client_configuration=False):
        return RequestsClient(timeout=timeout, cache=cache, max_retries=max_retries, backoff_factor=backoff_factor,
                              retry_statuses=retry_statuses, retry_methods=retry_methods, verify=verify,
                              http_client_instance=http_client_instance,
                              override_http_client_configuration=override_http_client_configuration,
                              response_factory=HttpResponseFactory())
