from apimatic_core.utilities.xml_helper import XmlHelper


class XMLModel(object):

    """Implementation of the 'AttributesAndElements' model.

    TODO: type model description here.

    Attributes:
        string_attr (string): string attribute (attribute name "string")
        number_attr (int): number attribute (attribute name "number")
        string_element (string): string element (element name "string")
        number_element (int): number element (element name "number")

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "string_attr": 'string-attr',
        "number_attr": 'number-attr',
        "boolean_attr": 'boolean-attr',
        "string_element": 'string-element',
        "number_element": 'number-element',
        "boolean_element": 'boolean-element',
        "elements": 'elements'
    }

    def __init__(self,
                 string_attr=None,
                 number_attr=None,
                 boolean_attr=None,
                 string_element=None,
                 number_element=None,
                 boolean_element=None,
                 elements=None):
        """Constructor for the AttributesAndElementsModel class"""

        # Initialize members of the class
        self.string_attr = string_attr 
        self.number_attr = number_attr
        self.boolean_attr = boolean_attr
        self.string_element = string_element 
        self.number_element = number_element
        self.boolean_element = boolean_element
        self.elements = elements

    @classmethod
    def from_element(cls, root):
        """Initialize an instance of this class using an xml.etree.Element.

        Args:
            root (string): The root xml element.

        Returns:
            object: An instance of this class.

        """
        string_attr = XmlHelper.value_from_xml_attribute(root.get('string'), str)
        number_attr = XmlHelper.value_from_xml_attribute(root.get('number'), int)
        boolean_attr = XmlHelper.value_from_xml_attribute(root.get('boolean'), bool)
        string_element = XmlHelper.value_from_xml_element(root.find('string'), str)
        number_element = XmlHelper.value_from_xml_element(root.find('number'), int)
        boolean_element = XmlHelper.value_from_xml_element(root.find('boolean'), bool)
        elements = XmlHelper.list_from_xml_element(
            root, 'item', str, wrapping_element_name='elements')
        return cls(string_attr,
                   number_attr,
                   boolean_attr,
                   string_element,
                   number_element,
                   boolean_element,
                   elements)

    def to_xml_sub_element(self, root):
        """Convert this object to an instance of xml.etree.Element.

        Args:
            root (xml.etree.Element): The parent of this xml element.
        """
        XmlHelper.add_as_attribute(root, self.string_attr, 'string')
        XmlHelper.add_as_attribute(root, self.number_attr, 'number')
        XmlHelper.add_as_attribute(root, self.boolean_attr, 'boolean')
        XmlHelper.add_as_subelement(root, self.string_element, 'string')
        XmlHelper.add_as_subelement(root, self.number_element, 'number')
        XmlHelper.add_as_subelement(root, self.boolean_element, 'boolean')
        XmlHelper.add_list_as_subelement(root, self.elements, 'item',
                                         wrapping_element_name='elements')
