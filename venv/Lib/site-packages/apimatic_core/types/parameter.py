
class Parameter:

    def get_key(self):
        return self._key

    def get_value(self):
        return self._value

    def need_to_encode(self):
        return self._should_encode

    def get_default_content_type(self):
        return self._default_content_type

    def __init__(
            self
    ):
        self._key = None
        self._value = None
        self._is_required = False
        self._should_encode = False
        self._default_content_type = None
        self._validator = None

    def key(self, key):
        self._key = key
        return self

    def value(self, value):
        self._value = value
        return self

    def is_required(self, is_required):
        self._is_required = is_required
        return self

    def should_encode(self, should_encode):
        self._should_encode = should_encode
        return self

    def default_content_type(self, default_content_type):
        self._default_content_type = default_content_type
        return self

    def validator(self, validator):
        self._validator = validator
        return self

    def validate(self):
        if self._is_required and self._value is None:
            raise ValueError("Required parameter {} cannot be None.".format(self._key))

        if self._validator is not None and self._validator(self._value):
            return

