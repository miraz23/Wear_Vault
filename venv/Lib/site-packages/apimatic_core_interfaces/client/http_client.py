# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class HttpClient(ABC):
    """An interface for the methods that an HTTP Client must implement

    This class should not be instantiated but should be used as a base class
    for HTTP Client classes.

    """

    @abstractmethod
    def execute(self, request, endpoint_configuration):
        """Execute a given CoreHttpRequest to get a string response back

        Args:
            request (HttpRequest): The given HttpRequest to execute.
            endpoint_configuration (EndpointConfiguration): The endpoint configurations to use.

        Returns:
            HttpResponse: The response of the CoreHttpRequest.

        """
        ...

    @abstractmethod
    def convert_response(self, response, contains_binary_response, request):
        """Converts the Response object of the HttpClient into an
        HttpResponse object.

        Args:
            response (dynamic): The original response object.
            contains_binary_response (bool): The flag to check if the response is of binary type.
            request (HttpRequest): The original HttpRequest object.

        Returns:
            HttpResponse: The converted HttpResponse object.

        """
        ...
