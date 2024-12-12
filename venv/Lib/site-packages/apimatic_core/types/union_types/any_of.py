from apimatic_core_interfaces.types.union_type import UnionType
from apimatic_core.types.union_types.union_type_context import UnionTypeContext
from apimatic_core.utilities.union_type_helper import UnionTypeHelper


class AnyOf(UnionType):

    def __init__(self, union_types, union_type_context: UnionTypeContext = UnionTypeContext()):
        super(AnyOf, self).__init__(union_types, union_type_context)
        self.collection_cases = None

    def validate(self, value):
        context = self._union_type_context
        UnionTypeHelper.update_nested_flag_for_union_types(self._union_types)
        is_optional_or_nullable = UnionTypeHelper.is_optional_or_nullable_case(context,
                                                                               [nested_type.get_context()
                                                                                for nested_type in self._union_types])

        if value is None and is_optional_or_nullable:
            self.is_valid = True
            return self

        if value is None:
            self.is_valid = False
            self.error_messages = UnionTypeHelper.process_errors(value, self._union_types, self.error_messages,
                                                                 self.get_context().is_nested, False)
            return self

        self._validate_value_against_case(value, context)

        if not self.is_valid:
            self.error_messages = UnionTypeHelper.process_errors(value, self._union_types, self.error_messages,
                                                                 self.get_context().is_nested, False)

        return self

    def deserialize(self, value):
        if value is None:
            return None

        return UnionTypeHelper.deserialize_value(value, self._union_type_context, self.collection_cases,
                                                 self._union_types)

    def _validate_value_against_case(self, value, context):
        if context.is_array() and context.is_dict() and context.is_array_of_dict():
            self.is_valid, self.collection_cases = UnionTypeHelper.validate_array_of_dict_case(self._union_types, value,
                                                                                               False)
        elif context.is_array() and context.is_dict():
            self.is_valid, self.collection_cases = UnionTypeHelper.validate_dict_of_array_case(self._union_types, value,
                                                                                               False)
        elif context.is_array():
            self.is_valid, self.collection_cases = UnionTypeHelper.validate_array_case(self._union_types, value, False)
        elif context.is_dict():
            self.is_valid, self.collection_cases = UnionTypeHelper.validate_dict_case(self._union_types, value, False)
        else:
            self.is_valid = UnionTypeHelper.get_matched_count(value, self._union_types, False) >= 1

    def __deepcopy__(self, memo={}):
        copy_object = AnyOf(self._union_types, self._union_type_context)
        copy_object.is_valid = self.is_valid
        copy_object.collection_cases = self.collection_cases
        copy_object.error_messages = self.error_messages
        return copy_object
