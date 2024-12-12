from abc import ABC, abstractmethod


class ResponseFactory(ABC):

    @abstractmethod
    def create(self, status_code, reason, headers, body, request):
        ...
