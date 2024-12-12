from apimatic_core.utilities.api_helper import ApiHelper
from tests.apimatic_core.mocks.union_type_lookup import UnionTypeLookUp


class UnionTypeScalarModel(object):

    """Implementation of the 'ScalarModel' model.

    This class contains scalar types in oneOf/anyOf cases.

    Attributes:
        any_of_required (float | bool): TODO: type description here.
        one_of_req_nullable (int | str | None): TODO: type description here.
        one_of_optional (int | float | str | None): TODO: type description
            here.
        any_of_opt_nullable (int | bool | None): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "any_of_required": 'anyOfRequired',
        "one_of_req_nullable": 'oneOfReqNullable',
        "one_of_optional": 'oneOfOptional',
        "any_of_opt_nullable": 'anyOfOptNullable'
    }

    _optionals = [
        'one_of_optional',
        'any_of_opt_nullable',
    ]

    _nullables = [
        'one_of_req_nullable',
        'any_of_opt_nullable',
    ]

    def __init__(self,
                 any_of_required=None,
                 one_of_req_nullable=None,
                 one_of_optional=ApiHelper.SKIP,
                 any_of_opt_nullable=ApiHelper.SKIP):
        """Constructor for the ScalarModel class"""

        # Initialize members of the class
        self.any_of_required = any_of_required
        self.one_of_req_nullable = one_of_req_nullable
        if one_of_optional is not ApiHelper.SKIP:
            self.one_of_optional = one_of_optional
        if any_of_opt_nullable is not ApiHelper.SKIP:
            self.any_of_opt_nullable = any_of_opt_nullable

    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object
            as obtained from the deserialization of the server's response. The
            keys MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        any_of_required = ApiHelper.deserialize_union_type(
            UnionTypeLookUp.get('ScalarModelAnyOfRequired'),
            dictionary.get('anyOfRequired'), False) if dictionary.get('anyOfRequired') is not None else None
        one_of_req_nullable = ApiHelper.deserialize_union_type(
            UnionTypeLookUp.get('ScalarModelOneOfReqNullable'),
            dictionary.get('oneOfReqNullable'), False) if dictionary.get('oneOfReqNullable') is not None else None
        one_of_optional = ApiHelper.deserialize_union_type(
            UnionTypeLookUp.get('ScalarModelOneOfOptional'),
            dictionary.get('oneOfOptional'), False) if dictionary.get('oneOfOptional') is not None else ApiHelper.SKIP
        if 'anyOfOptNullable' in dictionary.keys():
            any_of_opt_nullable = ApiHelper.deserialize_union_type(
                UnionTypeLookUp.get('ScalarModelAnyOfOptNullable'),
                dictionary.get('anyOfOptNullable'), False) if dictionary.get('anyOfOptNullable') is not None else None
        else:
            any_of_opt_nullable = ApiHelper.SKIP
        # Return an object of this model
        return cls(any_of_required,
                   one_of_req_nullable,
                   one_of_optional,
                   any_of_opt_nullable)

    @classmethod
    def validate(cls, dictionary):
        """Validates dictionary against class required properties

        Args:
            dictionary (dictionary): A dictionary representation of the object
            as obtained from the deserialization of the server's response. The
            keys MUST match property names in the API description.

        Returns:
            boolean : if dictionary is valid contains required properties.

        """
        if isinstance(dictionary, cls):
            return ApiHelper.is_valid_type(
                value=dictionary.any_of_required,
                type_callable=lambda value: UnionTypeLookUp.get('ScalarModelAnyOfRequired').validate) and \
                   ApiHelper.is_valid_type(
                       value=dictionary.one_of_req_nullable,
                       type_callable=lambda value: UnionTypeLookUp.get('ScalarModelOneOfReqNullable').validate)

        if not isinstance(dictionary, dict):
            return False

        return ApiHelper.is_valid_type(
            value=dictionary.get('anyOfRequired'),
            type_callable=lambda value: UnionTypeLookUp.get('ScalarModelAnyOfRequired').validate) and \
               ApiHelper.is_valid_type(
                   value=dictionary.get('oneOfReqNullable'),
                   type_callable=lambda value: UnionTypeLookUp.get('ScalarModelOneOfReqNullable').validate)
