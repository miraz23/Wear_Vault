import dateutil
from apimatic_core.utilities.api_helper import ApiHelper


class InnerComplexType(object):

    """Implementation of the 'InnerComplexType' model.

    TODO: type model description here.

    Attributes:
        string_type (str): TODO: type description here.
        boolean_type (bool): TODO: type description here.
        long_type (long|int): TODO: type description here.
        precision_type (float): TODO: type description here.
        string_list_type (list of str): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "boolean_type": 'booleanType',
        "date_time_type": 'dateTimeType',
        "date_type": 'dateType',
        "long_type": 'longType',
        "precision_type": 'precisionType',
        "string_list_type": 'stringListType',
        "string_type": 'stringType'
    }

    def __init__(self,
                 boolean_type=None,
                 long_type=None,
                 precision_type=None,
                 string_list_type=None,
                 string_type=None,
                 additional_properties={}):
        """Constructor for the InnerComplexType class"""

        # Initialize members of the class
        self.string_type = string_type
        self.boolean_type = boolean_type
        self.long_type = long_type
        self.precision_type = precision_type
        self.string_list_type = string_list_type

        # Add additional model properties to the instance
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
        boolean_type = dictionary.get("booleanType") if "booleanType" in dictionary.keys() else None
        long_type = dictionary.get("longType") if dictionary.get("longType") else None
        precision_type = dictionary.get("precisionType") if dictionary.get("precisionType") else None
        string_list_type = dictionary.get("stringListType") if dictionary.get("stringListType") else None
        string_type = dictionary.get("stringType") if dictionary.get("stringType") else None
        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]
        # Return an object of this model
        return cls(boolean_type,
                   long_type,
                   precision_type,
                   string_list_type,
                   string_type,
                   dictionary)
