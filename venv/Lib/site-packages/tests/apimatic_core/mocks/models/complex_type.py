from apimatic_core.utilities.api_helper import ApiHelper
from tests.apimatic_core.mocks.models.inner_complex_type import InnerComplexType


class ComplexType(object):

    """Implementation of the 'ComplexType' model.

    TODO: type model description here.

    Attributes:
        inner_complex_type (InnerComplexType): TODO: type description here.
        inner_complex_list_type (list of InnerComplexType): TODO: type
            description here.
        inner_complex_map_type (dict): TODO: type description here.
        inner_complex_list_of_map_type (list of InnerComplexType): TODO: type
            description here.
        inner_complex_map_of_list_type (list of InnerComplexType): TODO: type
            description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "inner_complex_list_type": 'innerComplexListType',
        "inner_complex_type": 'innerComplexType',
        "inner_complex_list_of_map_type": 'innerComplexListOfMapType',
        "inner_complex_map_of_list_type": 'innerComplexMapOfListType',
        "inner_complex_map_type": 'innerComplexMapType'
    }

    _optionals = [
        'inner_complex_map_type',
        'inner_complex_list_of_map_type',
        'inner_complex_map_of_list_type',
    ]

    def __init__(self,
                 inner_complex_list_type=None,
                 inner_complex_type=None,
                 inner_complex_list_of_map_type=ApiHelper.SKIP,
                 inner_complex_map_of_list_type=ApiHelper.SKIP,
                 inner_complex_map_type=ApiHelper.SKIP,
                 additional_properties={}):
        """Constructor for the ComplexType class"""

        # Initialize members of the class
        self.inner_complex_type = inner_complex_type
        self.inner_complex_list_type = inner_complex_list_type
        if inner_complex_map_type is not ApiHelper.SKIP:
            self.inner_complex_map_type = inner_complex_map_type
        if inner_complex_list_of_map_type is not ApiHelper.SKIP:
            self.inner_complex_list_of_map_type = inner_complex_list_of_map_type
        if inner_complex_map_of_list_type is not ApiHelper.SKIP:
            self.inner_complex_map_of_list_type = inner_complex_map_of_list_type

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
        inner_complex_list_type = None
        if dictionary.get('innerComplexListType') is not None:
            inner_complex_list_type = [InnerComplexType.from_dictionary(x) for x in dictionary.get('innerComplexListType')]
        inner_complex_type = InnerComplexType.from_dictionary(dictionary.get('innerComplexType')) if dictionary.get('innerComplexType') else None
        inner_complex_list_of_map_type = None
        if dictionary.get('innerComplexListOfMapType') is not None:
            inner_complex_list_of_map_type = [InnerComplexType.from_dictionary(x) for x in dictionary.get('innerComplexListOfMapType')]
        else:
            inner_complex_list_of_map_type = ApiHelper.SKIP
        inner_complex_map_of_list_type = None
        if dictionary.get('innerComplexMapOfListType') is not None:
            inner_complex_map_of_list_type = [InnerComplexType.from_dictionary(x) for x in dictionary.get('innerComplexMapOfListType')]
        else:
            inner_complex_map_of_list_type = ApiHelper.SKIP
        inner_complex_map_type = InnerComplexType.from_dictionary(dictionary.get('innerComplexMapType')) if 'innerComplexMapType' in dictionary.keys() else ApiHelper.SKIP
        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]
        # Return an object of this model
        return cls(inner_complex_list_type,
                   inner_complex_type,
                   inner_complex_list_of_map_type,
                   inner_complex_map_of_list_type,
                   inner_complex_map_type,
                   dictionary)
