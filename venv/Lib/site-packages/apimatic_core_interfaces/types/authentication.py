from abc import ABC, abstractmethod


class Authentication(ABC):

    @abstractmethod
    def is_valid(self):
        ...

    @abstractmethod
    def apply(self, http_request):
        ...
