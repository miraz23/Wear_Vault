class XmlAttributes:

    def get_value(self):
        return self._value

    def get_root_element_name(self):
        return self._root_element_name

    def get_array_item_name(self):
        return self._array_item_name

    def __init__(
            self
    ):
        self._value = None
        self._root_element_name = None
        self._array_item_name = None

    def value(self, value):
        self._value = value
        return self

    def root_element_name(self, root_element_name):
        self._root_element_name = root_element_name
        return self

    def array_item_name(self, array_item_name):
        self._array_item_name = array_item_name
        return self

