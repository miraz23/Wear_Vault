from apimatic_core.utilities.api_helper import ApiHelper


class Atom(object):

    """Implementation of the 'Atom' model.

    TODO: type model description here.

    Attributes:
        atom_number_of_electrons (int): TODO: type description here.
        atom_number_of_protons (int): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "atom_number_of_electrons": 'AtomNumberOfElectrons',
        "atom_number_of_protons": 'AtomNumberOfProtons'
    }

    _optionals = [
        'atom_number_of_protons',
    ]

    def __init__(self,
                 atom_number_of_electrons=None,
                 atom_number_of_protons=ApiHelper.SKIP):
        """Constructor for the Atom class"""

        # Initialize members of the class
        self.atom_number_of_electrons = atom_number_of_electrons
        if atom_number_of_protons is not ApiHelper.SKIP:
            self.atom_number_of_protons = atom_number_of_protons

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
        atom_number_of_electrons = dictionary.get("AtomNumberOfElectrons") if \
            dictionary.get("AtomNumberOfElectrons") else None
        atom_number_of_protons = dictionary.get("AtomNumberOfProtons") if \
            dictionary.get("AtomNumberOfProtons") else ApiHelper.SKIP
        # Return an object of this model
        return cls(atom_number_of_electrons,
                   atom_number_of_protons)

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
            return ApiHelper.is_valid_type(value=dictionary.atom_number_of_electrons,
                                           type_callable=lambda value: isinstance(value, int))

        if not isinstance(dictionary, dict):
            return False

        return ApiHelper.is_valid_type(value=dictionary.get('AtomNumberOfElectrons'),
                                       type_callable=lambda value: isinstance(value, int))

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.atom_number_of_electrons == other.atom_number_of_electrons and \
                   self.atom_number_of_protons == other.atom_number_of_protons
        return False
