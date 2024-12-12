from datetime import date, datetime
import pytest
import sys
from apimatic_core.utilities.api_helper import ApiHelper
import xml.etree.ElementTree as ET
from apimatic_core.utilities.xml_helper import XmlHelper
from tests.apimatic_core.base import Base
from tests.apimatic_core.mocks.models.cat_model import CatModel
from tests.apimatic_core.mocks.models.dog_model import DogModel
from tests.apimatic_core.mocks.models.one_of_xml import OneOfXML
from tests.apimatic_core.mocks.models.wolf_model import WolfModel
from tests.apimatic_core.mocks.models.xml_model import XMLModel


class TestXMLHelper:

    @pytest.mark.parametrize('input_value, root_element_name, expected_value', [
        (50, 'Number', '<Number>50</Number>'),
        ('50', 'String', '<String>50</String>'),
        (50.58, 'Decimal', '<Decimal>50.58</Decimal>'),
        (True, 'Boolean', '<Boolean>true</Boolean>'),
        (date(1994, 2, 13), 'Date', '<Date>1994-02-13</Date>'),
        (ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         'UnixDateTime', '<UnixDateTime>761117415</UnixDateTime>'),
        (ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         'HttpDateTime', '<HttpDateTime>{}</HttpDateTime>'
         .format(Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15)))),
        (ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
         'RFC3339DateTime', '<RFC3339DateTime>{}</RFC3339DateTime>'
         .format(Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15)))),
        (Base.xml_model(), 'Model',
         '<Model string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</Model>'),
    ])
    def test_serialize_to_xml(self, input_value, root_element_name, expected_value):
        if sys.version_info[1] == 7:
            expected_value = expected_value.replace('string="String" number="10000" boolean="false">',
                                                    'boolean="false" number="10000" string="String">')

        actual_value = XmlHelper.serialize_to_xml(input_value, root_element_name)
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, root_element_name, array_element_name, expected_value', [
        ([50, 60, 70], 'Numbers', 'Item', '<Numbers><Item>50</Item><Item>60</Item><Item>70</Item></Numbers>'),
        (['50', '60', '70'], 'Strings', 'Item',
         '<Strings><Item>50</Item><Item>60</Item><Item>70</Item></Strings>'),
        ([50.58, 60.58, 70.58], 'Decimals', 'Item',
         '<Decimals><Item>50.58</Item><Item>60.58</Item><Item>70.58</Item></Decimals>'),
        ([True, False, True], 'Booleans', 'Item',
         '<Booleans><Item>true</Item><Item>false</Item><Item>true</Item></Booleans>'),
        ([date(1994, 2, 13), date(1994, 2, 14), date(1994, 2, 15)],
         'Dates', 'Item', '<Dates>'
                          '<Item>1994-02-13</Item>'
                          '<Item>1994-02-14</Item>'
                          '<Item>1994-02-15</Item>'
                          '</Dates>'),
        ([ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
          ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 14, 5, 30, 15)),
          ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 15, 5, 30, 15))],
         'DateTimes', 'Item', '<DateTimes>'
                              '<Item>761117415</Item>'
                              '<Item>761203815</Item>'
                              '<Item>761290215</Item>'
                              '</DateTimes>'),
        ([ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
          ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
          ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))],
         'DateTimes', 'Item', "<DateTimes>"
                              f"<Item>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
                              f"<Item>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
                              f"<Item>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
                              "</DateTimes>"),
        ([ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
          ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
          ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))],
         'DateTimes', 'Item', "<DateTimes>"
                              f"<Item>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
                              f"<Item>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
                              f"<Item>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
                              "</DateTimes>"),
        ([Base.xml_model(), Base.xml_model(),
          Base.xml_model()], 'Models', 'Item',
         '<Models>'
         '<Item string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</Item>'
         '<Item string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</Item>'
         '<Item string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</Item>'
         '</Models>')
    ])
    def test_serialize_list_to_xml(self, input_value, root_element_name, array_element_name, expected_value):
        if sys.version_info[1] == 7:
            expected_value = expected_value.replace('string="String" number="10000" boolean="false">',
                                                    'boolean="false" number="10000" string="String">')
        actual_value = XmlHelper.serialize_list_to_xml(input_value, root_element_name, array_element_name)
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, root_element_name, expected_value', [
        ({'Item1': 50, 'Item2': 60, 'Item3': 70}, 'Dictionary',
         '<Dictionary><Item1>50</Item1><Item2>60</Item2><Item3>70</Item3></Dictionary>'),
        ({'Item1': '50', 'Item2': '60', 'Item3': '70'}, 'Dictionary',
         '<Dictionary><Item1>50</Item1><Item2>60</Item2><Item3>70</Item3></Dictionary>'),
        ({'Item1': 50.58, 'Item2': 60.58, 'Item3': 70.58}, 'Dictionary',
         '<Dictionary><Item1>50.58</Item1><Item2>60.58</Item2><Item3>70.58</Item3></Dictionary>'),
        ({'Item1': True, 'Item2': False, 'Item3': True}, 'Dictionary',
         '<Dictionary><Item1>true</Item1><Item2>false</Item2><Item3>true</Item3></Dictionary>'),
        ({'Item1': date(1994, 2, 13), 'Item2': date(1994, 2, 14), 'Item3': date(1994, 2, 15)},
         'Dictionary', '<Dictionary>'
                       '<Item1>1994-02-13</Item1>'
                       '<Item2>1994-02-14</Item2>'
                       '<Item3>1994-02-15</Item3>'
                       '</Dictionary>'),
        ({'Item1': ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
          'Item2': ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 14, 5, 30, 15)),
          'Item3': ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 15, 5, 30, 15))},
         'Dictionary', '<Dictionary>'
                       '<Item1>761117415</Item1>'
                       '<Item2>761203815</Item2>'
                       '<Item3>761290215</Item3>'
                       '</Dictionary>'),
        ({'Item1': ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
          'Item2': ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
          'Item3': ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))},
         'Dictionary', '<Dictionary>'
                       f"<Item1>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item1>"
                       f"<Item2>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item2>"
                       f"<Item3>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item3>"
                       '</Dictionary>'),
        ({'Item1': ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
          'Item2': ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
          'Item3': ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))},
         'Dictionary', '<Dictionary>'
                       f"<Item1>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item1>"
                       f"<Item2>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item2>"
                       f"<Item3>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item3>"
                       '</Dictionary>'),
        ({'Item1': Base.xml_model(), 'Item2': Base.xml_model(),
          'Item3': Base.xml_model()}, 'Dictionary',
         '<Dictionary>'
         '<Item1 string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</Item1>'
         '<Item2 string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</Item2>'
         '<Item3 string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</Item3>'
         '</Dictionary>'),
    ])
    def test_serialize_dictionary_to_xml(self, input_value, root_element_name, expected_value):
        if sys.version_info[1] == 7:
            expected_value = expected_value.replace('string="String" number="10000" boolean="false">',
                                                    'boolean="false" number="10000" string="String">')
        actual_value = XmlHelper.serialize_dict_to_xml(input_value, root_element_name)
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, root_element_name, expected_value', [
        (70, 'root', '<root>70</root>'),
        (70.887, 'root', '<root>70.887</root>'),
        (True, 'root', '<root>true</root>'),
        ('True', 'root', '<root>True</root>'),
    ])
    def test_add_to_element(self, input_value, root_element_name, expected_value):
        root_element = ET.Element(root_element_name)
        XmlHelper.add_to_element(root_element, input_value)
        actual_value = ET.tostring(root_element).decode()
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, root_element_name, attribute_name, expected_value', [
        (70, 'root', 'attribute', '<root attribute="70" />'),
        (70.887, 'root', 'attribute', '<root attribute="70.887" />'),
        (True, 'root', 'attribute', '<root attribute="true" />'),
        ('True', 'root', 'attribute', '<root attribute="True" />'),
    ])
    def test_add_as_attribute(self, input_value, root_element_name, attribute_name, expected_value):
        root_element = ET.Element(root_element_name)
        XmlHelper.add_as_attribute(root_element, input_value, attribute_name)
        actual_value = ET.tostring(root_element).decode()
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, root_element_name, element_name, expected_value', [
        (70, 'root', 'element', '<root><element>70</element></root>'),
        (70.887, 'root', 'element', '<root><element>70.887</element></root>'),
        (True, 'root', 'element', '<root><element>true</element></root>'),
        ('True', 'root', 'element', '<root><element>True</element></root>')
    ])
    def test_add_as_sub_element(self, input_value, root_element_name, element_name, expected_value):
        root_element = ET.Element(root_element_name)
        XmlHelper.add_as_subelement(root_element, input_value, element_name)
        actual_value = ET.tostring(root_element).decode()
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, root_element_name, item_name, wrapping_element_name, expected_value', [
        ([50, 60, 70], 'root', 'Item', 'Numbers',
         '<root><Numbers><Item>50</Item><Item>60</Item><Item>70</Item></Numbers></root>'),
        (['50', '60', '70'], 'root', 'Item', 'Strings',
         '<root><Strings><Item>50</Item><Item>60</Item><Item>70</Item></Strings></root>'),
        ([50.58, 60.58, 70.58], 'root', 'Item', 'Decimals',
         '<root><Decimals><Item>50.58</Item><Item>60.58</Item><Item>70.58</Item></Decimals></root>'),
        ([True, False, True], 'root', 'Item', 'Booleans',
         '<root><Booleans><Item>true</Item><Item>false</Item><Item>true</Item></Booleans></root>'),
        ([True, False, True], 'root', 'Item', None,
         '<root><Item>true</Item><Item>false</Item><Item>true</Item></root>')
    ])
    def test_add_list_as_sub_element(self, input_value, root_element_name, item_name, wrapping_element_name,
                                     expected_value):
        root_element = ET.Element(root_element_name)
        XmlHelper.add_list_as_subelement(root_element, input_value, item_name, wrapping_element_name)
        actual_value = ET.tostring(root_element).decode()
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, root_element_name, dictionary_name, expected_value', [
        ({'Item1': 50, 'Item2': 60, 'Item3': 70}, 'root', 'Dictionary',
         '<root><Dictionary><Item1>50</Item1><Item2>60</Item2><Item3>70</Item3></Dictionary></root>'),
        ({'Item': [50, 60, 70]}, 'root', 'Dictionary',
         '<root><Dictionary><Item>50</Item><Item>60</Item><Item>70</Item></Dictionary></root>'),
        ({'Item1': '50', 'Item2': '60', 'Item3': '70'}, 'root', 'Dictionary',
         '<root><Dictionary><Item1>50</Item1><Item2>60</Item2><Item3>70</Item3></Dictionary></root>'),
        ({'Item1': 50.58, 'Item2': 60.58, 'Item3': 70.58}, 'root', 'Dictionary',
         '<root><Dictionary><Item1>50.58</Item1><Item2>60.58</Item2><Item3>70.58</Item3></Dictionary></root>'),
        ({'Item1': True, 'Item2': False, 'Item3': True}, 'root', 'Dictionary',
         '<root><Dictionary><Item1>true</Item1><Item2>false</Item2><Item3>true</Item3></Dictionary></root>')
    ])
    def test_add_dict_as_sub_element(self, input_value, root_element_name, dictionary_name, expected_value):
        root_element = ET.Element(root_element_name)
        XmlHelper.add_dict_as_subelement(root_element, input_value, dictionary_name)
        actual_value = ET.tostring(root_element).decode()
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, clazz, root_element_name, expected_value', [
        ('<Number>50</Number>', int, 'Number', XmlHelper.serialize_to_xml(50, 'Number')),
        ('<String>50</String>', str, 'String', XmlHelper.serialize_to_xml('50', 'String')),
        ('<Decimal>50.58</Decimal>', float, 'Decimal', XmlHelper.serialize_to_xml(50.58, 'Decimal')),
        ('<Boolean>true</Boolean>', bool, 'Boolean', XmlHelper.serialize_to_xml(True, 'Boolean')),
        ('<Date>1994-02-13</Date>', date, 'Date', XmlHelper.serialize_to_xml(date(1994, 2, 13), 'Date')),
        ('<UnixDateTime>761117415</UnixDateTime>',
         ApiHelper.UnixDateTime, 'UnixDateTime',
         XmlHelper.serialize_to_xml(ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
                                    'UnixDateTime')),
        ('<HttpDateTime>{}</HttpDateTime>'.format(Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))),
         ApiHelper.HttpDateTime, 'HttpDateTime',
         XmlHelper.serialize_to_xml(ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
                                    'HttpDateTime')),
        ('<RFC3339DateTime>{}</RFC3339DateTime>'.format(Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))),
         ApiHelper.RFC3339DateTime, 'RFC3339DateTime',
         XmlHelper.serialize_to_xml(ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
                                    'RFC3339DateTime')),
        ('<Model string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</Model>', XMLModel, 'Model',
         XmlHelper.serialize_to_xml(Base.xml_model(), 'Model')),
        ('<Root>'
         '<Cat>'
         '<Meows>true</Meows>'
         '</Cat>'
         '<Cat>'
         '<Meows>false</Meows>'
         '</Cat></Root>', OneOfXML, 'Root',
         XmlHelper.serialize_to_xml(Base.one_of_xml_cat_model(), 'Root')),
        ('<Root>'
         '<Dog>'
         '<Barks>true</Barks>'
         '</Dog>'
         '</Root>', OneOfXML, 'Root',
         XmlHelper.serialize_to_xml(Base.one_of_xml_dog_model(), 'Root')),
        ('<Root>'
         '<Items>'
         '<Wolf><Howls>true</Howls></Wolf>'
         '<Wolf><Howls>false</Howls></Wolf>'
         '</Items>'
         '</Root>', OneOfXML, 'Root',
         XmlHelper.serialize_to_xml(Base.one_of_xml_wolf_model(), 'Root')),
        (None, None, None, None)
    ])
    def test_deserialize_xml(self, input_value, clazz, root_element_name, expected_value):
        actual_value = XmlHelper.deserialize_xml(input_value, clazz)
        if expected_value:
            assert XmlHelper.serialize_to_xml(actual_value, root_element_name) == expected_value
        else:
            assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, item_name, clazz, root_element_name, expected_value', [
        ('<Items><Item>50</Item><Item>60</Item><Item>70</Item></Items>', 'Item', int, 'Items',
         XmlHelper.serialize_list_to_xml([50, 60, 70], 'Items', 'Item')),
        ('<Items><Item>50</Item><Item>60</Item><Item>70</Item></Items>', 'Item', str, 'Items',
         XmlHelper.serialize_list_to_xml(['50', '60', '70'], 'Items', 'Item')),
        ('<Items><Item>50.58</Item><Item>60.58</Item><Item>70.58</Item></Items>', 'Item', float, 'Items',
         XmlHelper.serialize_list_to_xml([50.58, 60.58, 70.58], 'Items', 'Item')),
        ('<Items><Item>true</Item><Item>false</Item><Item>true</Item></Items>', 'Item', bool, 'Items',
         XmlHelper.serialize_list_to_xml([True, False, True], 'Items', 'Item')),
        ('<Items>'
         '<Item>1994-02-13</Item>'
         '<Item>1994-02-14</Item>'
         '<Item>1994-02-15</Item>'
         '</Items>', 'Item', date, 'Items',
         XmlHelper.serialize_list_to_xml([date(1994, 2, 13), date(1994, 2, 14), date(1994, 2, 15)], 'Items', 'Item')),
        ('<Items>'
         '<Item>761117415</Item>'
         '<Item>761203815</Item>'
         '<Item>761290215</Item>'
         '</Items>', 'Item', ApiHelper.UnixDateTime,
         'Items',
         XmlHelper.serialize_list_to_xml([ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
                                          ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 14, 5, 30, 15)),
                                          ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 15, 5, 30, 15))],
                                         'Items', 'Item')),
        ('<Items>'
         f"<Item>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
         f"<Item>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
         f"<Item>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
         '</Items>', 'Item', ApiHelper.HttpDateTime,
         'Items',
         XmlHelper.serialize_list_to_xml([ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
                                          ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
                                          ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))],
                                         'Items', 'Item')),
        ('<Items>'
         f"<Item>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
         f"<Item>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
         f"<Item>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item>"
         '</Items>', 'Item', ApiHelper.RFC3339DateTime,
         'Items',
         XmlHelper.serialize_list_to_xml([ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
                                          ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
                                          ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))],
                                         'Items', 'Item')),
        ('<Models>'
         '<Item string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</Item>'
         '<Item string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</Item>'
         '<Item string="String" number="10000" boolean="false">'
         '<string>Hey! I am being tested.</string>'
         '<number>5000</number>'
         '<boolean>false</boolean>'
         '<elements>'
         '<item>a</item>'
         '<item>b</item>'
         '<item>c</item>'
         '</elements>'
         '</Item>'
         '</Models>', 'Item', XMLModel,
         'Models',
         XmlHelper.serialize_list_to_xml([Base.xml_model(),
                                          Base.xml_model(),
                                          Base.xml_model()],
                                         'Models', 'Item')),
        (None, None, None, None, None)
    ])
    def test_deserialize_xml_to_list(self, input_value, item_name, clazz, root_element_name, expected_value):
        actual_value = XmlHelper.deserialize_xml_to_list(input_value, item_name, clazz)
        if expected_value:
            assert XmlHelper.serialize_list_to_xml(actual_value, root_element_name, item_name) == expected_value
        else:
            assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, clazz, root_element_name, expected_value', [
        ('<Items><Item1>50</Item1><Item2>60</Item2><Item3>70</Item3></Items>', int, 'Items',
         XmlHelper.serialize_dict_to_xml({'Item1': 50, 'Item2': 60, 'Item3': 70}, 'Items')),
        ('<Items><Item1>50</Item1><Item2>60</Item2><Item3>70</Item3></Items>', str, 'Items',
         XmlHelper.serialize_dict_to_xml({'Item1': '50', 'Item2': '60', 'Item3': '70'}, 'Items')),
        ('<Items><Item1>50.58</Item1><Item2>60.58</Item2><Item3>70.58</Item3></Items>', float, 'Items',
         XmlHelper.serialize_dict_to_xml({'Item1': 50.58, 'Item2': 60.58, 'Item3': 70.58}, 'Items')),
        ('<Items><Item1>true</Item1><Item2>false</Item2><Item3>true</Item3></Items>', bool, 'Items',
         XmlHelper.serialize_dict_to_xml({'Item1': True, 'Item2': False, 'Item3': True}, 'Items')),
        ('<Items>'
         '<Item1>1994-02-13</Item1>'
         '<Item2>1994-02-14</Item2>'
         '<Item3>1994-02-15</Item3>'
         '</Items>', date, 'Items',
         XmlHelper.serialize_dict_to_xml(
             {'Item1': date(1994, 2, 13), 'Item2': date(1994, 2, 14), 'Item3': date(1994, 2, 15)}, 'Items')),
        ('<Items>'
         '<Item1>761117415</Item1>'
         '<Item2>761203815</Item2>'
         '<Item3>761290215</Item3>'
         '</Items>', ApiHelper.UnixDateTime,
         'Items',
         XmlHelper.serialize_dict_to_xml(
             {'Item1': ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
              'Item2': ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 14, 5, 30, 15)),
              'Item3': ApiHelper.UnixDateTime.from_datetime(datetime(1994, 2, 15, 5, 30, 15))},
             'Items')),
        ('<Items>'
         f"<Item1>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item1>"
         f"<Item2>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item2>"
         f"<Item3>{Base.get_http_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item3>"
         '</Items>', ApiHelper.HttpDateTime,
         'Items',
         XmlHelper.serialize_dict_to_xml(
             {'Item1': ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
              'Item2': ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
              'Item3': ApiHelper.HttpDateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))},
             'Items')),
        ('<Items>'
         f"<Item1>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item1>"
         f"<Item2>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item2>"
         f"<Item3>{Base.get_rfc3339_datetime(datetime(1994, 2, 13, 5, 30, 15))}</Item3>"
         '</Items>', ApiHelper.RFC3339DateTime,
         'Items',
         XmlHelper.serialize_dict_to_xml(
             {'Item1': ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
              'Item2': ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15)),
              'Item3': ApiHelper.RFC3339DateTime.from_datetime(datetime(1994, 2, 13, 5, 30, 15))},
             'Items')),
        (None, None, None, None)
    ])
    def test_deserialize_xml_to_dict(self, input_value, clazz, root_element_name, expected_value):
        actual_value = XmlHelper.deserialize_xml_to_dict(input_value, clazz)
        if expected_value:
            assert XmlHelper.serialize_dict_to_xml(actual_value, root_element_name) == expected_value
        else:
            assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, clazz, expected_value', [
        ('True', str, 'True'),
        ('True', bool, True),
        ('70', int, 70),
        ('70.56443', float, 70.56443),
        (None, None, None),
    ])
    def test_value_from_xml_attribute(self, input_value, clazz, expected_value):
        actual_value = XmlHelper.value_from_xml_attribute(input_value, clazz)
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, clazz, root_element_name, expected_value', [
        ('True', str, 'root', 'True'),
        ('True', bool, 'root', True),
        ('70', int, 'root', 70),
        ('70.56443', float, 'root', 70.56443),
        (None, None, None, None),
    ])
    def test_value_from_xml_element(self, input_value, root_element_name, clazz, expected_value):
        root_element = None
        if input_value:
            root_element = ET.Element(root_element_name)
            XmlHelper.add_to_element(root_element, input_value)
        actual_value = XmlHelper.value_from_xml_element(root_element, clazz)
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, root_element_name, item_name, '
                             'wrapping_element_name, clazz, expected_value', [
                                 ([50, 60, 70], 'root', 'item', 'items', int, [50, 60, 70]),
                                 (['50', '60', '70'], 'root', 'item', 'items', str, ['50', '60', '70']),
                                 ([50.58, 60.58, 70.58], 'root', 'item', 'items', float, [50.58, 60.58, 70.58]),
                                 ([True, False, True], 'root', 'item', 'items', bool, [True, False, True]),
                                 ([True, False, True], 'root', 'item', 'items', bool, [True, False, True]),
                                 (None, None, None, None, None, None),
                             ])
    def test_list_from_xml_element(self, input_value, root_element_name, item_name,
                                   wrapping_element_name, clazz, expected_value):
        root_element = None
        if input_value:
            root_element = ET.Element(root_element_name)
            XmlHelper.add_list_as_subelement(root_element, input_value, item_name, wrapping_element_name)
        actual_value = XmlHelper.list_from_xml_element(root_element, item_name, clazz, wrapping_element_name)
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, root_element_name, item_name, '
                             'serialization_wrapping_element_name, deserialization_wrapping_element_name,'
                             'clazz, expected_value', [
                                 ([50, 60, 70], 'root', 'item', 'items', 'invalid_items', int, None),
                             ])
    def test_list_from_xml_element_with_unset_wrapper(self, input_value, root_element_name, item_name,
                                                      serialization_wrapping_element_name,
                                                      deserialization_wrapping_element_name,
                                                      clazz, expected_value):
        root_element = None
        if input_value:
            root_element = ET.Element(root_element_name)
            XmlHelper.add_list_as_subelement(root_element, input_value, item_name, serialization_wrapping_element_name)
        actual_value = XmlHelper.list_from_xml_element(root_element, item_name, clazz,
                                                       deserialization_wrapping_element_name)
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, wrapping_element_name, clazz, expected_value', [
        ({'Item1': 50, 'Item2': 60, 'Item3': 70}, 'items', int, {'Item1': 50, 'Item2': 60, 'Item3': 70}),
        ({'Item1': '50', 'Item2': '60', 'Item3': '70'}, 'items', str, {'Item1': '50', 'Item2': '60', 'Item3': '70'}),
        ({'Item1': 50.58, 'Item2': 60.58, 'Item3': 70.58}, 'items', float,
         {'Item1': 50.58, 'Item2': 60.58, 'Item3': 70.58}),
        ({'Item1': True, 'Item2': False, 'Item3': True}, 'items', bool, {'Item1': True, 'Item2': False, 'Item3': True}),
        ({'Item1': True, 'Item2': False, 'Item3': True}, 'items', bool, {'Item1': True, 'Item2': False, 'Item3': True}),
        (None, None, None, None),
    ])
    def test_dict_from_xml_element(self, input_value, wrapping_element_name,
                                   clazz, expected_value):
        root_element = None
        if input_value:
            root_element = ET.Element(wrapping_element_name)
            XmlHelper.add_dict_as_subelement(root_element, input_value)
        actual_value = XmlHelper.dict_from_xml_element(root_element, clazz)
        assert actual_value == expected_value

    @pytest.mark.parametrize('input_value, root_element_name, item_name, mapping_data, expected_value', [
        (Base.one_of_xml_dog_model(), 'root', 'Dog', {
            'Cat': (CatModel, True, None),
            'Dog': (DogModel, False, None),
            'Wolf': (WolfModel, True, 'Items'),
        }, '<root>'
           '<Dog><Barks>true</Barks></Dog>'
           '</root>'),
        (Base.one_of_xml_cat_model(), 'root', 'Cat', {
            'Cat': (CatModel, True, None),
            'Dog': (DogModel, False, None),
            'Wolf': (WolfModel, True, 'Items'),
        }, '<root>'
           '<Cat><Meows>true</Meows></Cat>'
           '<Cat><Meows>false</Meows></Cat>'
           '</root>'),
        (Base.one_of_xml_wolf_model(), 'root', 'Wolf', {
            'Cat': (CatModel, True, None),
            'Dog': (DogModel, False, None),
            'Wolf': (WolfModel, True, 'Items'),
        }, '<root>'
           '<Wolf><Howls>true</Howls></Wolf>'
           '<Wolf><Howls>false</Howls></Wolf>'
           '</root>'),
        (None, 'root', 'Wolf', {}, None)
    ])
    def test_list_from_multiple_one_of_xml_element(self, input_value, root_element_name, item_name,
                                                   mapping_data, expected_value):
        root_element = ET.Element(root_element_name)
        if input_value:
            XmlHelper.add_to_element(root_element, input_value)
        actual_value = XmlHelper.list_from_multiple_one_of_xml_element(root_element, mapping_data)
        if actual_value:
            assert XmlHelper.serialize_list_to_xml(actual_value, root_element_name, item_name) == expected_value
        else:
            assert input_value == expected_value

    @pytest.mark.parametrize('input_mapping_data, expected_output', [
        ({}, None),
        (None, None)
    ])
    def test_value_from_one_of_xml_elements(self, input_mapping_data, expected_output):
        assert XmlHelper.value_from_one_of_xml_elements(None, input_mapping_data) == expected_output
