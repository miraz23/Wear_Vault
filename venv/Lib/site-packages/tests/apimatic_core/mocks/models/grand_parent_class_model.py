from apimatic_core.utilities.api_helper import ApiHelper


class GrandParentClassModel(object):

    """Implementation of the 'Grand Parent Class' model.

    TODO: type model description here.

    Attributes:
        grand_parent_optional (string): TODO: type description here.
        grand_parent_required_nullable (string): TODO: type description here.
        grand_parent_required (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "grand_parent_required_nullable": 'Grand_Parent_Required_Nullable',
        "grand_parent_required": 'Grand_Parent_Required',
        "grand_parent_optional": 'Grand_Parent_Optional'
    }

    _optionals = [
        'grand_parent_optional',
    ]

    _nullables = [
        'grand_parent_required_nullable',
    ]

    def __init__(self,
                 grand_parent_required_nullable=None,
                 grand_parent_required='not nullable and required',
                 grand_parent_optional=ApiHelper.SKIP):
        """Constructor for the GrandParentClassModel class"""

        # Initialize members of the class
        if grand_parent_optional is not ApiHelper.SKIP:
            self.grand_parent_optional = grand_parent_optional
        self.grand_parent_required_nullable = grand_parent_required_nullable
        self.grand_parent_required = grand_parent_required

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

        grand_parent_required_nullable = dictionary.get("Grand_Parent_Required_Nullable") if dictionary.get("Grand_Parent_Required_Nullable") else None
        grand_parent_required = dictionary.get("Grand_Parent_Required") if dictionary.get("Grand_Parent_Required") else 'not nullable and required'
        grand_parent_optional = dictionary.get("Grand_Parent_Optional") if dictionary.get("Grand_Parent_Optional") else ApiHelper.SKIP
        # Return an object of this model
        return cls(grand_parent_required_nullable,
                   grand_parent_required,
                   grand_parent_optional)


class ParentClassModel(GrandParentClassModel):

    """Implementation of the 'Parent Class' model.

    TODO: type model description here.
    NOTE: This class inherits from 'GrandParentClassModel'.

    Attributes:
        mclass (int): TODO: type description here.
        precision (float): TODO: type description here.
        big_decimal (float): TODO: type description here.
        parent_optional_nullable_with_default_value (string): TODO: type
            description here.
        parent_optional (string): TODO: type description here.
        parent_required_nullable (string): TODO: type description here.
        parent_required (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "parent_required_nullable": 'Parent_Required_Nullable',
        "parent_required": 'Parent_Required',
        "grand_parent_required_nullable": 'Grand_Parent_Required_Nullable',
        "grand_parent_required": 'Grand_Parent_Required',
        "mclass": 'class',
        "precision": 'precision',
        "big_decimal": 'Big_Decimal',
        "parent_optional_nullable_with_default_value": 'Parent_Optional_Nullable_With_Default_Value',
        "parent_optional": 'Parent_Optional',
        "grand_parent_optional": 'Grand_Parent_Optional'
    }

    _optionals = [
        'mclass',
        'precision',
        'big_decimal',
        'parent_optional_nullable_with_default_value',
        'parent_optional',
    ]
    _optionals.extend(GrandParentClassModel._optionals)

    _nullables = [
        'mclass',
        'precision',
        'big_decimal',
        'parent_optional_nullable_with_default_value',
        'parent_required_nullable',
    ]
    _nullables.extend(GrandParentClassModel._nullables)

    def __init__(self,
                 parent_required_nullable=None,
                 parent_required='not nullable and required',
                 grand_parent_required_nullable=None,
                 grand_parent_required='not nullable and required',
                 mclass=23,
                 precision=ApiHelper.SKIP,
                 big_decimal=ApiHelper.SKIP,
                 parent_optional_nullable_with_default_value='Has default value',
                 parent_optional=ApiHelper.SKIP,
                 grand_parent_optional=ApiHelper.SKIP):
        """Constructor for the ParentClassModel class"""

        # Initialize members of the class
        self.mclass = mclass
        if precision is not ApiHelper.SKIP:
            self.precision = precision
        if big_decimal is not ApiHelper.SKIP:
            self.big_decimal = big_decimal
        self.parent_optional_nullable_with_default_value = parent_optional_nullable_with_default_value
        if parent_optional is not ApiHelper.SKIP:
            self.parent_optional = parent_optional
        self.parent_required_nullable = parent_required_nullable
        self.parent_required = parent_required

        # Call the constructor for the base class
        super(ParentClassModel, self).__init__(grand_parent_required_nullable,
                                               grand_parent_required,
                                               grand_parent_optional)

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

        parent_required_nullable = dictionary.get("Parent_Required_Nullable") if dictionary.get("Parent_Required_Nullable") else None
        parent_required = dictionary.get("Parent_Required") if dictionary.get("Parent_Required") else 'not nullable and required'
        grand_parent_required_nullable = dictionary.get("Grand_Parent_Required_Nullable") if dictionary.get("Grand_Parent_Required_Nullable") else None
        grand_parent_required = dictionary.get("Grand_Parent_Required") if dictionary.get("Grand_Parent_Required") else 'not nullable and required'
        mclass = dictionary.get("class") if dictionary.get("class") else 23
        precision = dictionary.get("precision") if "precision" in dictionary.keys() else ApiHelper.SKIP
        big_decimal = dictionary.get("Big_Decimal") if "Big_Decimal" in dictionary.keys() else ApiHelper.SKIP
        parent_optional_nullable_with_default_value = dictionary.get("Parent_Optional_Nullable_With_Default_Value") if dictionary.get("Parent_Optional_Nullable_With_Default_Value") else 'Has default value'
        parent_optional = dictionary.get("Parent_Optional") if dictionary.get("Parent_Optional") else ApiHelper.SKIP
        grand_parent_optional = dictionary.get("Grand_Parent_Optional") if dictionary.get("Grand_Parent_Optional") else ApiHelper.SKIP
        # Return an object of this model
        return cls(parent_required_nullable,
                   parent_required,
                   grand_parent_required_nullable,
                   grand_parent_required,
                   mclass,
                   precision,
                   big_decimal,
                   parent_optional_nullable_with_default_value,
                   parent_optional,
                   grand_parent_optional)


class ChildClassModel(ParentClassModel):

    """Implementation of the 'Child Class' model.

    TODO: type model description here.
    NOTE: This class inherits from 'ParentClassModel'.

    Attributes:
        optional_nullable (string): TODO: type description here.
        optional_nullable_with_default_value (string): TODO: type description
            here.
        optional (string): TODO: type description here.
        required_nullable (string): TODO: type description here.
        required (string): TODO: type description here.
        child_class_array (list of ChildClassModel): TODO: type description
            here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "required_nullable": 'Required_Nullable',
        "required": 'Required',
        "parent_required_nullable": 'Parent_Required_Nullable',
        "parent_required": 'Parent_Required',
        "grand_parent_required_nullable": 'Grand_Parent_Required_Nullable',
        "grand_parent_required": 'Grand_Parent_Required',
        "optional_nullable": 'Optional_Nullable',
        "optional_nullable_with_default_value": 'Optional_Nullable_With_Default_Value',
        "optional": 'Optional',
        "child_class_array": 'Child_Class_Array',
        "mclass": 'class',
        "precision": 'precision',
        "big_decimal": 'Big_Decimal',
        "parent_optional_nullable_with_default_value": 'Parent_Optional_Nullable_With_Default_Value',
        "parent_optional": 'Parent_Optional',
        "grand_parent_optional": 'Grand_Parent_Optional'
    }

    _optionals = [
        'optional_nullable',
        'optional_nullable_with_default_value',
        'optional',
        'child_class_array',
    ]
    _optionals.extend(ParentClassModel._optionals)

    _nullables = [
        'optional_nullable',
        'optional_nullable_with_default_value',
        'required_nullable',
        'child_class_array',
    ]
    _nullables.extend(ParentClassModel._nullables)

    def __init__(self,
                 required,
                 required_nullable=None,
                 parent_required_nullable=None,
                 parent_required='not nullable and required',
                 grand_parent_required_nullable=None,
                 grand_parent_required='not nullable and required',
                 optional_nullable=ApiHelper.SKIP,
                 optional_nullable_with_default_value='With default value',
                 optional=ApiHelper.SKIP,
                 child_class_array=ApiHelper.SKIP,
                 mclass=23,
                 precision=ApiHelper.SKIP,
                 big_decimal=ApiHelper.SKIP,
                 parent_optional_nullable_with_default_value='Has default value',
                 parent_optional=ApiHelper.SKIP,
                 grand_parent_optional=ApiHelper.SKIP):
        """Constructor for the ChildClassModel class"""

        # Initialize members of the class
        if optional_nullable is not ApiHelper.SKIP:
            self.optional_nullable = optional_nullable
        self.optional_nullable_with_default_value = optional_nullable_with_default_value
        if optional is not ApiHelper.SKIP:
            self.optional = optional
        self.required_nullable = required_nullable
        self.required = required
        if child_class_array is not ApiHelper.SKIP:
            self.child_class_array = child_class_array

        # Call the constructor for the base class
        super(ChildClassModel, self).__init__(parent_required_nullable,
                                              parent_required,
                                              grand_parent_required_nullable,
                                              grand_parent_required,
                                              mclass,
                                              precision,
                                              big_decimal,
                                              parent_optional_nullable_with_default_value,
                                              parent_optional,
                                              grand_parent_optional)

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

        required_nullable = dictionary.get("Required_Nullable") if dictionary.get("Required_Nullable") else None
        required = dictionary.get("Required")
        parent_required_nullable = dictionary.get("Parent_Required_Nullable") if dictionary.get("Parent_Required_Nullable") else None
        parent_required = dictionary.get("Parent_Required") if dictionary.get("Parent_Required") else 'not nullable and required'
        grand_parent_required_nullable = dictionary.get("Grand_Parent_Required_Nullable") if dictionary.get("Grand_Parent_Required_Nullable") else None
        grand_parent_required = dictionary.get("Grand_Parent_Required") if dictionary.get("Grand_Parent_Required") else 'not nullable and required'
        optional_nullable = dictionary.get("Optional_Nullable") if "Optional_Nullable" in dictionary.keys() else ApiHelper.SKIP
        optional_nullable_with_default_value = dictionary.get("Optional_Nullable_With_Default_Value") if dictionary.get("Optional_Nullable_With_Default_Value") else 'With default value'
        optional = dictionary.get("Optional") if dictionary.get("Optional") else ApiHelper.SKIP
        if 'Child_Class_Array' in dictionary.keys():
            child_class_array = [ChildClassModel.from_dictionary(x) for x in dictionary.get('Child_Class_Array')] if dictionary.get('Child_Class_Array') else None
        else:
            child_class_array = ApiHelper.SKIP
        mclass = dictionary.get("class") if dictionary.get("class") else 23
        precision = dictionary.get("precision") if "precision" in dictionary.keys() else ApiHelper.SKIP
        big_decimal = dictionary.get("Big_Decimal") if "Big_Decimal" in dictionary.keys() else ApiHelper.SKIP
        parent_optional_nullable_with_default_value = dictionary.get("Parent_Optional_Nullable_With_Default_Value") if dictionary.get("Parent_Optional_Nullable_With_Default_Value") else 'Has default value'
        parent_optional = dictionary.get("Parent_Optional") if dictionary.get("Parent_Optional") else ApiHelper.SKIP
        grand_parent_optional = dictionary.get("Grand_Parent_Optional") if dictionary.get("Grand_Parent_Optional") else ApiHelper.SKIP
        # Return an object of this model
        return cls(required,
                   required_nullable,
                   parent_required_nullable,
                   parent_required,
                   grand_parent_required_nullable,
                   grand_parent_required,
                   optional_nullable,
                   optional_nullable_with_default_value,
                   optional,
                   child_class_array,
                   mclass,
                   precision,
                   big_decimal,
                   parent_optional_nullable_with_default_value,
                   parent_optional,
                   grand_parent_optional)