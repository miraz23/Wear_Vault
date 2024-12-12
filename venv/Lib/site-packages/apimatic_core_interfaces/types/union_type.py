from abc import ABC, abstractmethod


class UnionType(ABC):
    NATIVE_TYPES = [int, str, float, bool]

    def __init__(self, union_types, union_type_context):
        self._union_types = union_types
        self._union_type_context = union_type_context
        self.is_valid = False
        self.error_messages = set()

    @abstractmethod
    def validate(self, value):
        ...

    @abstractmethod
    def deserialize(self, value):
        ...

    def get_context(self):
        return self._union_type_context
