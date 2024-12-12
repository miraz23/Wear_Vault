from apimatic_core.utilities.xml_helper import XmlHelper


class DogModel(object):

    """Implementation of the 'Dog' model.

    TODO: type model description here.

    Attributes:
        barks (bool): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "barks": 'Barks'
    }

    def __init__(self,
                 barks=None):
        """Constructor for the DogModel class"""

        # Initialize members of the class
        self.barks = barks

    @classmethod
    def from_element(cls, root):
        """Initialize an instance of this class using an xml.etree.Element.

        Args:
            root (string): The root xml element.

        Returns:
            object: An instance of this class.

        """
        barks = XmlHelper.value_from_xml_element(root.find('Barks'), bool)

        return cls(barks)

    def to_xml_sub_element(self, root):
        """Convert this object to an instance of xml.etree.Element.

        Args:
            root (xml.etree.Element): The parent of this xml element.
        """
        XmlHelper.add_as_subelement(root, self.barks, 'Barks')
