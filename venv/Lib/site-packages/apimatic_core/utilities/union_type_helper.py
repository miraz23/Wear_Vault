import copy
from datetime import datetime
from apimatic_core.exceptions.anyof_validation_exception import AnyOfValidationException
from apimatic_core.exceptions.oneof_validation_exception import OneOfValidationException
from apimatic_core.types.datetime_format import DateTimeFormat
from apimatic_core.utilities.api_helper import ApiHelper
from apimatic_core.utilities.datetime_helper import DateTimeHelper


class UnionTypeHelper:

    NONE_MATCHED_ERROR_MESSAGE = 'We could not match any acceptable types against the given JSON.'
    MORE_THAN_1_MATCHED_ERROR_MESSAGE = 'There are more than one acceptable type matched against the given JSON.'

    @staticmethod
    def get_deserialized_value(union_types, value):
        return [union_type for union_type in union_types if union_type.is_valid][0].deserialize(value)

    @staticmethod
    def validate_array_of_dict_case(union_types, array_value, is_for_one_of):
        if UnionTypeHelper.is_invalid_array_value(array_value):
            return tuple((False, []))

        collection_cases = []
        valid_cases = []
        for item in array_value:
            case_validity, inner_dictionary = UnionTypeHelper.validate_dict_case(union_types, item, is_for_one_of)
            collection_cases.append(inner_dictionary)
            valid_cases.append(case_validity)
        is_valid = sum(valid_cases) == array_value.__len__()
        return tuple((is_valid, collection_cases))

    @staticmethod
    def validate_dict_of_array_case(union_types, dict_value, is_for_one_of):
        if UnionTypeHelper.is_invalid_dict_value(dict_value):
            return tuple((False, []))

        collection_cases = {}
        valid_cases = []
        for key, item in dict_value.items():
            case_validity, inner_array = UnionTypeHelper.validate_array_case(union_types, item, is_for_one_of)
            collection_cases[key] = inner_array
            valid_cases.append(case_validity)
        is_valid = sum(valid_cases) == dict_value.__len__()
        return tuple((is_valid, collection_cases))

    @staticmethod
    def validate_dict_case(union_types, dict_value, is_for_one_of):
        if UnionTypeHelper.is_invalid_dict_value(dict_value):
            return tuple((False, []))

        is_valid, collection_cases = UnionTypeHelper.process_dict_items(union_types, dict_value, is_for_one_of)

        return tuple((is_valid, collection_cases))

    @staticmethod
    def process_dict_items(union_types, dict_value, is_for_one_of):
        is_valid = True
        collection_cases = {}

        for key, value in dict_value.items():
            union_type_cases = UnionTypeHelper.make_deep_copies(union_types)
            matched_count = UnionTypeHelper.get_matched_count(value, union_type_cases, is_for_one_of)
            is_valid = UnionTypeHelper.check_item_validity(is_for_one_of, is_valid, matched_count)
            collection_cases[key] = union_type_cases

        return is_valid, collection_cases

    @staticmethod
    def validate_array_case(union_types, array_value, is_for_one_of):
        if UnionTypeHelper.is_invalid_array_value(array_value):
            return tuple((False, []))

        is_valid, collection_cases = UnionTypeHelper.process_array_items(union_types, array_value, is_for_one_of)

        return tuple((is_valid, collection_cases))

    @staticmethod
    def process_array_items(union_types, array_value, is_for_one_of):
        is_valid = True
        collection_cases = []

        for item in array_value:
            union_type_cases = UnionTypeHelper.make_deep_copies(union_types)
            matched_count = UnionTypeHelper.get_matched_count(item, union_type_cases, is_for_one_of)
            is_valid = UnionTypeHelper.check_item_validity(is_for_one_of, is_valid, matched_count)
            collection_cases.append(union_type_cases)

        return is_valid, collection_cases

    @staticmethod
    def check_item_validity(is_for_one_of, is_valid, matched_count):
        if is_valid and is_for_one_of:
            is_valid = matched_count == 1
        elif is_valid:
            is_valid = matched_count >= 1
        return is_valid

    @staticmethod
    def make_deep_copies(union_types):
        nested_cases = []
        for union_type in union_types:
            nested_cases.append(copy.deepcopy(union_type))

        return nested_cases

    @staticmethod
    def get_matched_count(value, union_types, is_for_one_of):
        matched_count = UnionTypeHelper.get_valid_cases_count(value, union_types)

        if is_for_one_of and matched_count == 1:
            return matched_count
        elif not is_for_one_of and matched_count > 0:
            return matched_count

        matched_count = UnionTypeHelper.handle_discriminator_cases(value, union_types)
        return matched_count

    @staticmethod
    def get_valid_cases_count(value, union_types):
        return sum(union_type.validate(value).is_valid for union_type in union_types)

    @staticmethod
    def handle_discriminator_cases(value, union_types):
        has_discriminator_cases = all(union_type.get_context().get_discriminator() is not None and
                                      union_type.get_context().get_discriminator_value() is not None
                                      for union_type in union_types)

        if has_discriminator_cases:
            for union_type in union_types:
                union_type.get_context().discriminator(None)
                union_type.get_context().discriminator_value(None)

            return UnionTypeHelper.get_valid_cases_count(value, union_types)

        return 0

    @staticmethod
    def validate_date_time(value, context):
        if isinstance(value, ApiHelper.RFC3339DateTime):
            return context.get_date_time_format() == DateTimeFormat.RFC3339_DATE_TIME

        if isinstance(value, ApiHelper.HttpDateTime):
            return context.get_date_time_format() == DateTimeFormat.HTTP_DATE_TIME

        if isinstance(value, ApiHelper.UnixDateTime):
            return context.get_date_time_format() == DateTimeFormat.UNIX_DATE_TIME

        if isinstance(value, datetime) and context.get_date_time_converter() is not None:
            serialized_dt = str(ApiHelper.when_defined(context.get_date_time_converter(), value))
            return DateTimeHelper.validate_datetime(serialized_dt, context.get_date_time_format())

        return DateTimeHelper.validate_datetime(value, context.get_date_time_format())

    @staticmethod
    def is_optional_or_nullable_case(current_context, inner_contexts):
        return current_context.is_nullable_or_optional() or \
               any(context.is_nullable_or_optional() for context in inner_contexts)

    @staticmethod
    def update_nested_flag_for_union_types(nested_union_types):
        for union_type in nested_union_types:
            union_type.get_context().is_nested = True

    @staticmethod
    def is_invalid_array_value(value):
        return value is None or not isinstance(value, list)

    @staticmethod
    def is_invalid_dict_value(value):
        return value is None or not isinstance(value, dict)

    @staticmethod
    def deserialize_value(value, context, collection_cases, union_types):
        if context.is_array() and context.is_dict() and context.is_array_of_dict():
            return UnionTypeHelper.deserialize_array_of_dict_case(value, collection_cases)

        if context.is_array() and context.is_dict():
            return UnionTypeHelper.deserialize_dict_of_array_case(value, collection_cases)

        if context.is_array():
            return UnionTypeHelper.deserialize_array_case(value, collection_cases)

        if context.is_dict():
            return UnionTypeHelper.deserialize_dict_case(value, collection_cases)

        return UnionTypeHelper.get_deserialized_value(union_types, value)

    @staticmethod
    def deserialize_array_of_dict_case(array_value, collection_cases):
        deserialized_value = []
        for index, item in enumerate(array_value):
            deserialized_value.append(UnionTypeHelper.deserialize_dict_case(item, collection_cases[index]))

        return deserialized_value

    @staticmethod
    def deserialize_dict_of_array_case(dict_value, collection_cases):
        deserialized_value = {}
        for key, value in dict_value.items():
            deserialized_value[key] = UnionTypeHelper.deserialize_array_case(value, collection_cases[key])

        return deserialized_value

    @staticmethod
    def deserialize_dict_case(dict_value, collection_cases):
        deserialized_value = {}
        for key, value in dict_value.items():
            valid_case = [case for case in collection_cases[key] if case.is_valid][0]
            deserialized_value[key] = valid_case.deserialize(value)

        return deserialized_value

    @staticmethod
    def deserialize_array_case(array_value, collection_cases):
        deserialized_value = []
        for index, item in enumerate(array_value):
            valid_case = [case for case in collection_cases[index] if case.is_valid][0]
            deserialized_value.append(valid_case.deserialize(item))

        return deserialized_value

    @staticmethod
    def process_errors(value, union_types, error_messages, is_nested, is_for_one_of):
        error_messages.add(', '.join(UnionTypeHelper.get_combined_error_messages(union_types)))

        if not is_nested:
            UnionTypeHelper.raise_validation_exception(value, union_types, ', '.join(error_messages), is_for_one_of)

        return error_messages

    @staticmethod
    def get_combined_error_messages(union_types):
        combined_error_messages = []
        from apimatic_core.types.union_types.leaf_type import LeafType
        for union_type in union_types:
            if isinstance(union_type, LeafType):
                combined_error_messages.append(union_type.type_to_match.__name__)
            elif union_type.error_messages:
                combined_error_messages.append(', '.join(union_type.error_messages))
        return combined_error_messages

    @staticmethod
    def raise_validation_exception(value, union_types, error_message, is_for_one_of):
        if is_for_one_of:
            matched_count = sum(union_type.is_valid for union_type in union_types)
            message = UnionTypeHelper.MORE_THAN_1_MATCHED_ERROR_MESSAGE if matched_count > 0 \
                else UnionTypeHelper.NONE_MATCHED_ERROR_MESSAGE
            raise OneOfValidationException('{} \nActual Value: {}\nExpected Type: One Of {}.'.format(
                message, value, error_message))
        else:
            raise AnyOfValidationException('{} \nActual Value: {}\nExpected Type: Any Of {}.'.format(
                UnionTypeHelper.NONE_MATCHED_ERROR_MESSAGE, value, error_message))
