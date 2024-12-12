from apimatic_core.utilities.xml_helper import XmlHelper


class WolfModel(object):

    """Implementation of the 'Wolf' model.

    TODO: type model description here.

    Attributes:
        howls (bool): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "howls": 'Howls'
    }

    def __init__(self,
                 howls=None):
        """Constructor for the WolfModel class"""

        # Initialize members of the class
        self.howls = howls

    @classmethod
    def from_element(cls, root):
        """Initialize an instance of this class using an xml.etree.Element.

        Args:
            root (string): The root xml element.

        Returns:
            object: An instance of this class.

        """
        howls = XmlHelper.value_from_xml_element(root.find('Howls'), bool)

        return cls(howls)

    def to_xml_sub_element(self, root):
        """Convert this object to an instance of xml.etree.Element.

        Args:
            root (xml.etree.Element): The parent of this xml element.
        """
        XmlHelper.add_as_subelement(root, self.howls, 'Howls')
