from apimatic_core_interfaces.factories.response_factory import ResponseFactory

from tests.apimatic_requests_client_adapter.models.internal.http_response import HttpResponse


class HttpResponseFactory(ResponseFactory):

    def __init__(self):
        pass

    def create(self, status_code, reason_phrase, headers, body, request):
        return HttpResponse(status_code, reason_phrase, headers, body, request)
