from apimatic_core.utilities.api_helper import ApiHelper


class Lion(object):

    """Implementation of the 'Lion' model.

    TODO: type model description here.

    Attributes:
        id (int): TODO: type description here.
        weight (int): TODO: type description here.
        mtype (str): TODO: type description here.
        kind (str): TODO: type description here.

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
        """Validates dictionary against class required properties

        Args:
            dictionary (dictionary): A dictionary representation of the object
            as obtained from the deserialization of the server's response. The
            keys MUST match property names in the API description.

        Returns:
            boolean : if dictionary is valid contains required properties.

        """

        if isinstance(dictionary, cls):
            return ApiHelper.is_valid_type(value=dictionary.id, type_callable=lambda value: isinstance(value, int)) \
                and ApiHelper.is_valid_type(value=dictionary.weight, type_callable=lambda value: isinstance(value, int)) \
                and ApiHelper.is_valid_type(value=dictionary.mtype, type_callable=lambda value: isinstance(value, str))

        if not isinstance(dictionary, dict):
            return False

        return ApiHelper.is_valid_type(value=dictionary.get('id'), type_callable=lambda value: isinstance(value, int)) \
            and ApiHelper.is_valid_type(value=dictionary.get('weight'), type_callable=lambda value: isinstance(value, int)) \
            and ApiHelper.is_valid_type(value=dictionary.get('type'), type_callable=lambda value: isinstance(value, str))
