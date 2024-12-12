
class UnionTypeContext:

    @classmethod
    def create(cls, is_array=False, is_dict=False, is_array_of_dict=False, is_optional=False, is_nullable=False,
               discriminator=None, discriminator_value=None, date_time_format=None, date_time_converter=None):
        return cls().array(is_array).dict(is_dict)\
            .array_of_dict(is_array_of_dict)\
            .optional(is_optional)\
            .nullable(is_nullable)\
            .discriminator(discriminator)\
            .discriminator_value(discriminator_value)\
            .date_time_format(date_time_format)\
            .date_time_converter(date_time_converter)

    def __init__(self):
        self._is_array = False
        self._is_dict = False
        self._is_array_of_dict = False
        self._is_optional = False
        self._is_nullable = False
        self._discriminator = None
        self._discriminator_value = None
        self._date_time_format = None
        self._date_time_converter = None
        self.path = None
        self.is_nested = False

    def array(self, is_array):
        self._is_array = is_array
        return self

    def is_array(self):
        return self._is_array

    def dict(self, is_dict):
        self._is_dict = is_dict
        return self

    def is_dict(self):
        return self._is_dict

    def array_of_dict(self, is_array_of_dict):
        self._is_array_of_dict = is_array_of_dict
        return self

    def is_array_of_dict(self):
        return self._is_array_of_dict

    def optional(self, is_optional):
        self._is_optional = is_optional
        return self

    def is_optional(self):
        return self._is_optional

    def nullable(self, is_nullable):
        self._is_nullable = is_nullable
        return self

    def is_nullable(self):
        return self._is_nullable

    def is_nullable_or_optional(self):
        return self.is_nullable() or self.is_optional()

    def discriminator(self, discriminator):
        self._discriminator = discriminator
        return self

    def get_discriminator(self):
        return self._discriminator

    def discriminator_value(self, discriminator_value):
        self._discriminator_value = discriminator_value
        return self

    def get_discriminator_value(self):
        return self._discriminator_value

    def date_time_format(self, date_time_format):
        self._date_time_format = date_time_format
        return self

    def get_date_time_format(self):
        return self._date_time_format

    def date_time_converter(self, date_time_converter):
        self._date_time_converter = date_time_converter
        return self

    def get_date_time_converter(self):
        return self._date_time_converter

