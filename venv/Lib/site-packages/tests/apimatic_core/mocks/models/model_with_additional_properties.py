# -*- coding: utf-8 -*-
from tests.apimatic_core.mocks.union_type_lookup import UnionTypeLookUp
from tests.apimatic_core.mocks.models.lion import Lion
from apimatic_core.utilities.api_helper import ApiHelper


class ModelWithAdditionalPropertiesOfPrimitiveType(object):

    """Implementation of the 'NonInheritEnabledNumber' model.

    TODO: type model description here.

    Attributes:
        email (str): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "email": 'email'
    }

    def __init__(self,
                 email=None,
                 additional_properties=None):
        """Constructor for the NonInheritEnabledNumber class
        Args:
            email (str): TODO: type description here.
            additional_properties (dict[str, int]): TODO: type description here.
        """

        # Initialize members of the class
        if additional_properties is None:
            additional_properties = {}
        self.email = email
        self.additional_properties = additional_properties

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
        email = dictionary.get("email") if dictionary.get("email") else None

        additional_properties = ApiHelper.get_additional_properties(
            dictionary={k: v for k, v in dictionary.items() if k not in cls._names.values()},
            unboxing_function=lambda x: int(x))

        # Return an object of this model
        return cls(email, additional_properties)


class ModelWithAdditionalPropertiesOfPrimitiveArrayType(object):

    """Implementation of the 'NonInheritEnabledNumber' model.

    TODO: type model description here.

    Attributes:
        email (str): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "email": 'email'
    }

    def __init__(self,
                 email=None,
                 additional_properties=None):
        """Constructor for the NonInheritEnabledNumber class

        Args:
            email (str): TODO: type description here.
            additional_properties (dict[str, list[int]]): TODO: type description here.

        """

        # Initialize members of the class
        if additional_properties is None:
            additional_properties = {}
        self.email = email
        self.additional_properties = additional_properties

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
        email = dictionary.get("email") if dictionary.get("email") else None

        additional_properties = ApiHelper.get_additional_properties(
            dictionary={k: v for k, v in dictionary.items() if k not in cls._names.values()},
            unboxing_function=lambda x: ApiHelper.apply_unboxing_function(x, lambda item: int(item), is_array=True))

        # Return an object of this model
        return cls(email, additional_properties)

class ModelWithAdditionalPropertiesOfPrimitiveDictType(object):

    """Implementation of the 'NonInheritEnabledNumber' model.

    TODO: type model description here.

    Attributes:
        email (str): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "email": 'email'
    }

    def __init__(self,
                 email=None,
                 additional_properties=None):
        """Constructor for the NonInheritEnabledNumber class

        Args:
            email (str): TODO: type description here.
            additional_properties (dict[str, dict[str, int]]): TODO: type description here.

        """

        # Initialize members of the class
        if additional_properties is None:
            additional_properties = {}
        self.email = email
        self.additional_properties = additional_properties

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
        email = dictionary.get("email") if dictionary.get("email") else None

        additional_properties = ApiHelper.get_additional_properties(
            dictionary={k: v for k, v in dictionary.items() if k not in cls._names.values()},
            unboxing_function=lambda x: ApiHelper.apply_unboxing_function(x, lambda item: int(item), is_dict=True))

        # Return an object of this model
        return cls(email, additional_properties)

class ModelWithAdditionalPropertiesOfModelType(object):

    """Implementation of the 'NonInheritEnabledNumber' model.

    TODO: type model description here.

    Attributes:
        email (str): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "email": 'email'
    }

    def __init__(self,
                 email=None,
                 additional_properties=None):
        """Constructor for the NonInheritEnabledNumber class

        Args:
            email (str): TODO: type description here.
            additional_properties (dict[str, Lion]): TODO: type description here.

        """

        # Initialize members of the class
        if additional_properties is None:
            additional_properties = {}
        self.email = email
        self.additional_properties = additional_properties

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
        email = dictionary.get("email") if dictionary.get("email") else None

        additional_properties = ApiHelper.get_additional_properties(
            dictionary={k: v for k, v in dictionary.items() if k not in cls._names.values()},
            unboxing_function=lambda x: ApiHelper.apply_unboxing_function(x, lambda item: Lion.from_dictionary(item)))

        # Return an object of this model
        return cls(email, additional_properties)

class ModelWithAdditionalPropertiesOfModelArrayType(object):

    """Implementation of the 'NonInheritEnabledNumber' model.

    TODO: type model description here.

    Attributes:
        email (str): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "email": 'email'
    }

    def __init__(self,
                 email=None,
                 additional_properties=None):
        """Constructor for the NonInheritEnabledNumber class

        Args:
            email (str): TODO: type description here.
            additional_properties (dict[str, list[Lion]]): TODO: type description here.

        """

        # Initialize members of the class
        if additional_properties is None:
            additional_properties = {}
        self.email = email
        self.additional_properties = additional_properties

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
        email = dictionary.get("email") if dictionary.get("email") else None

        additional_properties = ApiHelper.get_additional_properties(
            dictionary={k: v for k, v in dictionary.items() if k not in cls._names.values()},
            unboxing_function=lambda x: ApiHelper.apply_unboxing_function(x, lambda item: Lion.from_dictionary(item), is_array=True))

        # Return an object of this model
        return cls(email, additional_properties)

class ModelWithAdditionalPropertiesOfModelDictType(object):

    """Implementation of the 'NonInheritEnabledNumber' model.

    TODO: type model description here.

    Attributes:
        email (str): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "email": 'email'
    }

    def __init__(self,
                 email=None,
                 additional_properties=None):
        """Constructor for the NonInheritEnabledNumber class

        Args:
            email (str): TODO: type description here.
            additional_properties (dict[str, dict[str, Lion]]): TODO: type description here.

        """

        # Initialize members of the class
        if additional_properties is None:
            additional_properties = {}
        self.email = email
        self.additional_properties = additional_properties

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
        email = dictionary.get("email") if dictionary.get("email") else None

        additional_properties = ApiHelper.get_additional_properties(
            dictionary={k: v for k, v in dictionary.items() if k not in cls._names.values()},
            unboxing_function=lambda x: ApiHelper.apply_unboxing_function(
                x, lambda item: Lion.from_dictionary(item),
                is_dict=True))

        # Return an object of this model
        return cls(email, additional_properties)

class ModelWithAdditionalPropertiesOfTypeCombinatorPrimitive(object):

    """Implementation of the 'NonInheritEnabledNumber' model.

    TODO: type model description here.

    Attributes:
        email (str): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "email": 'email'
    }

    def __init__(self,
                 email=None,
                 additional_properties=None):
        """Constructor for the NonInheritEnabledNumber class

        Args:
            email (str): TODO: type description here.
            additional_properties (dict[str, float|bool]): TODO: type description here.

        """

        # Initialize members of the class
        if additional_properties is None:
            additional_properties = {}
        self.email = email
        self.additional_properties = additional_properties

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
        email = dictionary.get("email") if dictionary.get("email") else None

        additional_properties = ApiHelper.get_additional_properties(
            dictionary={k: v for k, v in dictionary.items() if k not in cls._names.values()},
            unboxing_function=lambda x: ApiHelper.deserialize_union_type(UnionTypeLookUp.get('ScalarModelAnyOfRequired'),
                                                                         x, False))

        # Return an object of this model
        return cls(email, additional_properties)