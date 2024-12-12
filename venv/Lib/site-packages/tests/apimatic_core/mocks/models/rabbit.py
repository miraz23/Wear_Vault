from apimatic_core.utilities.api_helper import ApiHelper


class Rabbit(object):
    """Implementation of the 'Lion' model.

    TODO: type model description here.

    Attributes:
        id (string): TODO: type description here.
        weight (string): TODO: type description here.
        mtype (string): TODO: type description here.
        kind (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "id": 'id',
        "weight": 'weight',
        "mtype": 'type',
        "kind": 'kind'
    }

    _optionals = [
        'kind',
    ]

    def __init__(self,
                 id=None,
                 weight=None,
                 mtype=None,
                 kind=ApiHelper.SKIP):
        """Constructor for the Lion class"""

        # Initialize members of the class
        self.id = id
        self.weight = weight
        self.mtype = mtype
        if kind is not ApiHelper.SKIP:
            self.kind = kind

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

        id = dictionary.get("id") if dictionary.get("id") else None
        weight = dictionary.get("weight") if dictionary.get("weight") else None
        mtype = dictionary.get("type") if dictionary.get("type") else None
        kind = dictionary.get("kind") if dictionary.get("kind") else ApiHelper.SKIP
        # Return an object of this model
        return cls(id,
                   weight,
                   mtype,
                   kind)

    @classmethod
    def validate(cls, dictionary):
        """Validates dictionary against class properties.

        Args:
            dictionary: the dictionary to be validated against.

        Returns:
            boolean : if value is valid for this model.

        """
        if isinstance(dictionary, cls):
            return True

        if not isinstance(dictionary, dict):
            return False

        return dictionary.get("id") is not None and \
               ApiHelper.is_valid_type(dictionary.get("id"), lambda value: isinstance(value, str)) and \
               dictionary.get("weight") is not None and \
               ApiHelper.is_valid_type(dictionary.get("weight"), lambda value: isinstance(value, str)) and \
               dictionary.get("type") is not None and \
               ApiHelper.is_valid_type(dictionary.get("type"), lambda value: isinstance(value, str))
