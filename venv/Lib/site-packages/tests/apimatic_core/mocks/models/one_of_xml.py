from apimatic_core.utilities.xml_helper import XmlHelper
from tests.apimatic_core.mocks.models.cat_model import CatModel
from tests.apimatic_core.mocks.models.dog_model import DogModel
from tests.apimatic_core.mocks.models.wolf_model import WolfModel


class OneOfXML(object):
    """Implementation of the 'CatsOrADogOrWolves' model.

    Case 3

    Attributes:
        value (object): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "value": 'value'
    }

    def __init__(self,
                 value=None):
        """Constructor for the CatsOrADogOrWolvesModel class"""

        # Initialize members of the class
        self.value = value

    @classmethod
    def from_element(cls, root):
        """Initialize an instance of this class using an xml.etree.Element.

        Args:
            root (string): The root xml element.

        Returns:
            object: An instance of this class.

        """
        value = XmlHelper.value_from_one_of_xml_elements(
            root,
            {
                'Cat': (CatModel, True, None),
                'Dog': (DogModel, False, None),
                'Wolf': (WolfModel, True, 'Items'),
            }
        )

        return cls(value)

    def to_xml_sub_element(self, root):
        """Convert this object to an instance of xml.etree.Element.

        Args:
            root (xml.etree.Element): The parent of this xml element.
        """
        if type(self.value) is list and type(self.value[0]) is CatModel:
            XmlHelper.add_list_as_subelement(root, self.value, 'Cat')
        if type(self.value) is DogModel:
            XmlHelper.add_as_subelement(root, self.value, 'Dog')
        if type(self.value) is list and type(self.value[0]) is WolfModel:
            XmlHelper.add_list_as_subelement(root, self.value, 'Wolf',
                                             wrapping_element_name='Items')
