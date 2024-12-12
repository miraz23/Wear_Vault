from apimatic_core.utilities.xml_helper import XmlHelper


class CatModel(object):

    """Implementation of the 'Cat' model.

    TODO: type model description here.

    Attributes:
        meows (bool): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "meows": 'Meows'
    }

    def __init__(self,
                 meows=None):
        """Constructor for the CatModel class"""

        # Initialize members of the class
        self.meows = meows

    @classmethod
    def from_element(cls, root):
        """Initialize an instance of this class using an xml.etree.Element.

        Args:
            root (string): The root xml element.

        Returns:
            object: An instance of this class.

        """
        meows = XmlHelper.value_from_xml_element(root.find('Meows'), bool)

        return cls(meows)

    def to_xml_sub_element(self, root):
        """Convert this object to an instance of xml.etree.Element.

        Args:
            root (xml.etree.Element): The parent of this xml element.
        """
        XmlHelper.add_as_subelement(root, self.meows, 'Meows')
