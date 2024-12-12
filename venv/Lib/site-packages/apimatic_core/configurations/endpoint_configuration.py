
class EndpointConfiguration:

    @property
    def contains_binary_response(self):
        return self._has_binary_response

    @property
    def should_retry(self):
        return self._to_retry

    def __init__(
            self
    ):
        self._has_binary_response = None
        self._to_retry = None

    def has_binary_response(self, has_binary_response):
        self._has_binary_response = has_binary_response
        return self

    def to_retry(self, to_retry):
        self._to_retry = to_retry
        return self

