from apimatic_core.utilities.api_helper import ApiHelper


class Validate(object):

    """Implementation of the 'validate' model.

    TODO: type model description here.

    Attributes:
        field (string): TODO: type description here.
        name (string): TODO: type description here.
        address (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "field": 'field',
        "name": 'name',
        "address": 'address'
    }

    _optionals = [
        'address',
    ]

    def __init__(self,
                 field=None,
                 name=None,
                 address=ApiHelper.SKIP,
                 additional_properties={}):
        """Constructor for the Validate class"""

        # Initialize members of the class
        self.field = field 
        self.name = name 
        if address is not ApiHelper.SKIP:
            self.address = address 

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

        field = dictionary.get("field") if dictionary.get("field") else None
        name = dictionary.get("name") if dictionary.get("name") else None
        address = dictionary.get("address") if dictionary.get("address") else ApiHelper.SKIP
        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]
        # Return an object of this model
        return cls(field,
                   name,
                   address,
                   dictionary)
