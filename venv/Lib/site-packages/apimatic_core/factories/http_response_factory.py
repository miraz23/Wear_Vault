from apimatic_core_interfaces.factories.response_factory import ResponseFactory
from apimatic_core.http.response.http_response import HttpResponse


class HttpResponseFactory(ResponseFactory):

    def __init__(self):
        pass

    def create(self, status_code, reason, headers, body, request):
        return HttpResponse(status_code, reason, headers, body, request)
