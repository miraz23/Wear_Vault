from apimatic_core.utilities.api_helper import ApiHelper


class Orbit(object):

    """Implementation of the 'Orbit' model.

    TODO: type model description here.

    Attributes:
        orbit_number_of_electrons (int): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "orbit_number_of_electrons": 'OrbitNumberOfElectrons'
    }

    def __init__(self,
                 orbit_number_of_electrons=None):
        """Constructor for the Orbit class"""

        # Initialize members of the class
        self.orbit_number_of_electrons = orbit_number_of_electrons

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
        orbit_number_of_electrons = dictionary.get("OrbitNumberOfElectrons") \
            if dictionary.get("OrbitNumberOfElectrons") else None
        # Return an object of this model
        return cls(orbit_number_of_electrons)

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
            return ApiHelper.is_valid_type(value=dictionary.orbit_number_of_electrons,
                                           type_callable=lambda value: isinstance(value, int))

        if not isinstance(dictionary, dict):
            return False

        return ApiHelper.is_valid_type(value=dictionary.get('OrbitNumberOfElectrons'),
                                       type_callable=lambda value: isinstance(value, int))

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.orbit_number_of_electrons == other.orbit_number_of_electrons
        return False
