# -*- coding: utf-8 -*-
from collections import abc
import re
import datetime
import calendar
import email.utils as eut
from time import mktime
from urllib.parse import urlsplit

import jsonpickle
import dateutil.parser
from jsonpointer import JsonPointerException, resolve_pointer
from apimatic_core.types.datetime_format import DateTimeFormat
from apimatic_core.types.file_wrapper import FileWrapper
from apimatic_core.types.array_serialization_format import SerializationFormats
from requests.utils import quote


class ApiHelper(object):
    """A Helper Class for various functions associated with API Calls.

    This class contains static methods for operations that need to be
    performed during API requests. All of the methods inside this class are
    static methods, there is no need to ever initialise an instance of this
    class.

    """

    SKIP = '#$%^S0K1I2P3))*'

    @staticmethod
    def json_serialize_wrapped_params(obj):
        """JSON Serialization of a given wrapped object.

        Args:
            obj (object): The object to serialize.

        Returns:
            str: The JSON serialized string of the object.

        """
        if obj is None:
            return None
        val = dict()
        for k, v in obj.items():
            val[k] = ApiHelper.json_serialize(v, should_encode=False)

        return jsonpickle.encode(val, False)

    @staticmethod
    def json_serialize(obj, should_encode=True):
        """JSON Serialization of a given object.

        Args:
            obj (object): The object to serialize.
            should_encode: whether to encode at end or not

        Returns:
            str: The JSON serialized string of the object.

        """

        if obj is None:
            return None

        if isinstance(obj, str):
            return obj

        # Resolve any Names if it's one of our objects that needs to have this called on
        if isinstance(obj, list):
            value = list()
            for item in obj:
                if isinstance(item, dict) or isinstance(item, list):
                    value.append(ApiHelper.json_serialize(item, False))
                elif hasattr(item, "_names"):
                    value.append(ApiHelper.to_dictionary(item))
                else:
                    value.append(item)
            obj = value
        elif isinstance(obj, dict):
            value = dict()
            for key, item in obj.items():
                if isinstance(item, list) or isinstance(item, dict):
                    value[key] = ApiHelper.json_serialize(item, False)
                elif hasattr(item, "_names"):
                    value[key] = ApiHelper.to_dictionary(item)
                else:
                    value[key] = item
            obj = value
        else:
            if hasattr(obj, "_names"):
                obj = ApiHelper.to_dictionary(obj)
        if not should_encode:
            return obj
        return jsonpickle.encode(obj, False)

    @staticmethod
    def json_deserialize(json, unboxing_function=None, as_dict=False):
        """JSON Deserialization of a given string.

        Args:
            json (str): The JSON serialized string to deserialize.
            unboxing_function (callable): The deserialization funtion to be used.
            as_dict (bool): The flag to determine to deserialize json as dictionary type

        Returns:
            dict: A dictionary representing the data contained in the
                JSON serialized string.

        """
        if json is None or json.strip() == '':
            return None

        try:
            decoded = jsonpickle.decode(json)
        except ValueError:
            return json

        if unboxing_function is None:
            return decoded

        if as_dict:
            return {k: unboxing_function(v) for k, v in decoded.items()}
        elif isinstance(decoded, list):
            return [unboxing_function(element) for element in decoded]

        return unboxing_function(decoded)

    @staticmethod
    def apply_unboxing_function(value, unboxing_function, is_array=False, is_dict=False, is_array_of_map=False,
                                is_map_of_array=False, dimension_count=1):
        if is_dict:
            if is_map_of_array:
                return {k: ApiHelper.apply_unboxing_function(v,
                                                             unboxing_function,
                                                             is_array=True,
                                                             dimension_count=dimension_count)
                        for k, v in value.items()}
            else:
                return {k: unboxing_function(v) for k, v in value.items()}
        elif is_array:
            if is_array_of_map:
                return [
                    ApiHelper.apply_unboxing_function(element,
                                                      unboxing_function,
                                                      is_dict=True,
                                                      dimension_count=dimension_count)
                    for element in value]
            elif dimension_count > 1:
                return [ApiHelper.apply_unboxing_function(element, unboxing_function,
                                                          is_array=True,
                                                          dimension_count=dimension_count - 1)
                        for element in value]
            else:
                return [unboxing_function(element) for element in value]

        return unboxing_function(value)

    @staticmethod
    def dynamic_deserialize(dynamic_response):
        """JSON Deserialization of a given string.

        Args:
            dynamic_response (str): The response string to deserialize.

        Returns:
            dict: A dictionary representing the data contained in the
                JSON serialized string.


        """
        if dynamic_response is not None or not str(dynamic_response):
            return ApiHelper.json_deserialize(dynamic_response)

    @staticmethod
    def date_deserialize(response):
        """JSON Deserialization of a given string.

        Args:
            json (str): The JSON serialized string to deserialize.

        Returns:
            dict: A dictionary representing the data contained in the
                JSON serialized string.

        """
        deserialized_response = ApiHelper.json_deserialize(response)
        if isinstance(deserialized_response, list):
            return [dateutil.parser.parse(element).date() for element in deserialized_response]

        return dateutil.parser.parse(deserialized_response).date()

    @staticmethod
    def datetime_deserialize(response, datetime_format):
        """JSON Deserialization of a given string.

        Args:
            response: the response to deserialize
           datetime_format: The date time format to deserialize into

        Returns:
            dict: A dictionary representing the data contained in the
                JSON serialized string.

        """
        if response is None:
            return None

        if isinstance(response, str):
            deserialized_response = ApiHelper.json_deserialize(response)
        else:
            deserialized_response = response

        if DateTimeFormat.HTTP_DATE_TIME == datetime_format:
            if isinstance(deserialized_response, list):
                return [element.datetime for element in
                        ApiHelper.json_deserialize(response, ApiHelper.HttpDateTime.from_value)]
            else:
                return ApiHelper.HttpDateTime.from_value(response).datetime
        elif DateTimeFormat.UNIX_DATE_TIME == datetime_format:
            if isinstance(deserialized_response, list):
                return [element.datetime for element in
                        ApiHelper.json_deserialize(response, ApiHelper.UnixDateTime.from_value)]
            else:
                return ApiHelper.UnixDateTime.from_value(response).datetime
        elif DateTimeFormat.RFC3339_DATE_TIME == datetime_format:
            if isinstance(deserialized_response, list):
                return [element.datetime for element in
                        ApiHelper.json_deserialize(response, ApiHelper.RFC3339DateTime.from_value)]
            else:
                return ApiHelper.RFC3339DateTime.from_value(response).datetime

    @staticmethod
    def deserialize_union_type(union_type, response, should_deserialize=True):
        if should_deserialize:
            response = ApiHelper.json_deserialize(response, as_dict=True)

        union_type_result = union_type.validate(response)

        return union_type_result.deserialize(response)

    @staticmethod
    def get_content_type(value):
        """Get content type header for oneof.

        Args:
            value: The value passed by the user.

        Returns:
            dict: A dictionary representing the data contained in the
                JSON serialized string.

        """
        if value is None:
            return None
        primitive = (int, str, bool, float)

        if type(value) in primitive:
            return 'text/plain; charset=utf-8'

        else:
            return 'application/json; charset=utf-8'

    @staticmethod
    def get_schema_path(path, file_name):
        """Return the Schema's path

        Returns:
            string : returns Correct schema path

        """
        pascal_name = file_name.replace("_", " ").title().replace(" ", "")
        path = path.replace('\\models', '\\schemas').replace('/models', '/schemas') \
            .replace(".py", ".json").replace(file_name, pascal_name)
        return path

    @staticmethod
    def serialize_array(key, array, formatting="indexed", is_query=False):
        """Converts an array parameter to a list of key value tuples.

        Args:
            key (str): The name of the parameter.
            array (list): The value of the parameter.
            formatting (str): The type of key formatting expected.
            is_query (bool): Decides if the parameters are for query or form.

        Returns:
            list: A list with key value tuples for the array elements.

        """
        tuples = []

        serializable_types = (str, int, float, bool, datetime.date, ApiHelper.CustomDate)

        if isinstance(array[0], serializable_types):
            if formatting == SerializationFormats.UN_INDEXED:
                tuples += [("{0}[]".format(key), element) for element in array]
            elif formatting == SerializationFormats.INDEXED:
                tuples += [("{0}[{1}]".format(key, index), element) for index, element in enumerate(array)]
            elif formatting == SerializationFormats.PLAIN:
                tuples += [(key, element) for element in array]
            elif is_query:
                if formatting == SerializationFormats.CSV:
                    tuples += [(key, ",".join(str(x) for x in array))]

                elif formatting == SerializationFormats.PSV:
                    tuples += [(key, "|".join(str(x) for x in array))]

                elif formatting == SerializationFormats.TSV:
                    tuples += [(key, "\t".join(str(x) for x in array))]
                else:
                    raise ValueError("Invalid format provided.")
            else:
                raise ValueError("Invalid format provided.")
        else:
            tuples += [("{0}[{1}]".format(key, index), element) for index, element in enumerate(array)]

        return tuples

    @staticmethod
    def append_url_with_template_parameters(url, parameters):
        """Replaces template parameters in the given url.

        Args:
            url (str): The query url string to replace the template parameters.
            parameters (dict): The parameters to replace in the url.

        Returns:
            str: URL with replaced parameters.

        """
        # Parameter validation
        if url is None:
            raise ValueError("URL is None.")
        if parameters is None:
            return url

        # Iterate and replace parameters
        for key in parameters:
            value = parameters[key]['value']
            encode = parameters[key]['encode']
            replace_value = ''

            # Load parameter value
            if value is None:
                replace_value = ''
            elif isinstance(value, list):
                replace_value = "/".join((quote(str(x), safe='') if encode else str(x)) for x in value)
            else:
                replace_value = quote(str(value), safe='') if encode else str(value)

            url = url.replace('{{{0}}}'.format(key), str(replace_value))

        return url

    @staticmethod
    def append_url_with_query_parameters(url, parameters, array_serialization="indexed"):
        """Adds query parameters to a URL.

        Args:
            url (str): The URL string.
            parameters (dict): The query parameters to add to the URL.
            array_serialization (str): The format of array parameter serialization.

        Returns:
            str: URL with added query parameters.

        """
        # Parameter validation
        if url is None:
            raise ValueError("URL is None.")
        if parameters is None:
            return url
        parameters = ApiHelper.process_complex_types_parameters(parameters, array_serialization)
        for value in parameters:
            key = value[0]
            val = value[1]
            seperator = '&' if '?' in url else '?'
            if value is not None:
                url += "{0}{1}={2}".format(seperator, key, quote(str(val), safe=''))

        return url

    @staticmethod
    def get_url_without_query(url):
        """
        Extracts the protocol, domain, and path from a URL excluding the query parameters.

        Args:
            url: The URL string.

        Returns:
            A string containing the protocol, domain, and path of the URL without the query string.

        Raises:
            ValueError: If the URL is invalid.
        """
        try:
            parsed_url = urlsplit(url)
            if not parsed_url.netloc:  # Check if URL has scheme and netloc (valid URL)
                raise ValueError("Invalid URL format")
            return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        except ValueError as e:
            raise ValueError(f"Error parsing URL: {e}") from e

    @staticmethod
    def process_complex_types_parameters(query_parameters, array_serialization):
        processed_params = []
        for key, value in query_parameters.items():
            processed_params.extend(
                ApiHelper.form_encode(value, key, array_serialization=array_serialization, is_query=True))
        return processed_params

    @staticmethod
    def clean_url(url):
        """Validates and processes the given query Url to clean empty slashes.

        Args:
            url (str): The given query Url to process.

        Returns:
            str: Clean Url as string.

        """
        # Ensure that the urls are absolute
        regex = "^https?://[^/]+"
        match = re.match(regex, url)
        if match is None:
            raise ValueError('Invalid Url format.')

        protocol = match.group(0)
        index = url.find('?')
        query_url = url[len(protocol): index if index != -1 else None]
        query_url = re.sub("//+", "/", query_url)
        parameters = url[index:] if index != -1 else ""

        return protocol + query_url + parameters

    @staticmethod
    def form_encode_parameters(form_parameters, array_serialization="indexed"):
        """Form encodes a dictionary of form parameters

        Args:
            form_parameters (dictionary): The given dictionary which has
            atleast one model to form encode.
            array_serialization (str): The format of array parameter serialization.

        Returns:
            dict: A dictionary of form encoded properties of the model.

        """
        encoded = []

        for key, value in form_parameters.items():
            encoded += ApiHelper.form_encode(value, key, array_serialization)

        return encoded

    @staticmethod
    def form_encode(obj,
                    instance_name,
                    array_serialization="indexed", is_query=False):
        """Encodes a model in a form-encoded manner such as person[Name]

        Args:
            obj (object): The given Object to form encode.
            instance_name (string): The base name to appear before each entry
                for this object.
            array_serialization (string): The format of array parameter serialization.
            is_query (bool): Decides if the parameters are for query or form.

        Returns:
            dict: A dictionary of form encoded properties of the model.

        """
        retval = []
        # If we received an object, resolve it's field names.
        if hasattr(obj, "_names"):
            obj = ApiHelper.to_dictionary(obj)

        if obj is None:
            return []
        elif isinstance(obj, list):
            for element in ApiHelper.serialize_array(instance_name, obj, array_serialization, is_query):
                retval += ApiHelper.form_encode(element[1], element[0], array_serialization, is_query)
        elif isinstance(obj, dict):
            for item in obj:
                retval += ApiHelper.form_encode(obj[item], instance_name + "[" + item + "]", array_serialization,
                                                is_query)
        else:
            if isinstance(obj, bool):
                obj = str(obj).lower()
            retval.append((instance_name, obj))

        return retval

    @staticmethod
    def to_dictionary(obj, should_ignore_null_values=False):
        """Creates a dictionary representation of a class instance. The
        keys are taken from the API description and may differ from language
        specific variable names of properties.

        Args:
            obj: The object to be converted into a dictionary.
            should_ignore_null_values: Flag to ignore null values from the object dictionary

        Returns:
            dictionary: A dictionary form of the model with properties in
            their API formats.

        """
        dictionary = dict()

        optional_fields = obj._optionals if hasattr(obj, "_optionals") else []
        nullable_fields = obj._nullables if hasattr(obj, "_nullables") else []

        if hasattr(obj, 'validate'):
            obj.validate(obj)

        # Loop through all properties in this model
        names = {k: v for k, v in obj.__dict__.items() if v is not None} if should_ignore_null_values else obj._names
        for name in names:
            value = getattr(obj, name, ApiHelper.SKIP)

            if value is ApiHelper.SKIP:
                continue

            if value is None:
                if name not in optional_fields and not name in nullable_fields:
                    raise ValueError(f"The value for {name} can not be None for {obj}")
                else:
                    dictionary[obj._names[name]] = None
            elif isinstance(value, list):
                # Loop through each item
                dictionary[obj._names[name]] = list()
                for item in value:
                    if isinstance(item, list) or isinstance(item, dict):
                        dictionary[obj._names[name]].append(ApiHelper.process_nested_collection(
                            item, should_ignore_null_values))
                    else:
                        dictionary[obj._names[name]].append(ApiHelper.to_dictionary(item, should_ignore_null_values)
                                                            if hasattr(item, "_names") else item)
            elif isinstance(value, dict):
                # Loop through each item
                dictionary[obj._names[name]] = dict()
                for k, v in value.items():
                    if isinstance(v, list) or isinstance(v, dict):
                        dictionary[obj._names[name]][k] = ApiHelper.process_nested_collection(
                            v, should_ignore_null_values)
                    else:
                        dictionary[obj._names[name]][k] = ApiHelper.to_dictionary(value[k], should_ignore_null_values) \
                            if hasattr(value[k], "_names") else value[k]
            else:
                dictionary[obj._names[name]] = ApiHelper.to_dictionary(value, should_ignore_null_values) if \
                    hasattr(value, "_names") else value

        # Loop through all additional properties in this model
        if hasattr(obj, "additional_properties"):
            for name in obj.additional_properties:

                if name in dictionary.keys():
                    raise ValueError(f'An additional property key, \'{name}\' conflicts with one of the model\'s properties')

                value = obj.additional_properties.get(name)
                if isinstance(value, list):
                    # Loop through each item
                    dictionary[name] = list()
                    for item in value:
                        dictionary[name].append(
                            ApiHelper.to_dictionary(item, should_ignore_null_values) if hasattr(item, "_names") else item)
                elif isinstance(value, dict):
                    # Loop through each item
                    dictionary[name] = dict()
                    for key in value:
                        dictionary[name][key] = ApiHelper.to_dictionary(value[key], should_ignore_null_values) if hasattr(value[key],
                                                                                               "_names") else \
                            value[key]
                else:
                    dictionary[name] = ApiHelper.to_dictionary(value, should_ignore_null_values) if hasattr(value,
                                                                                 "_names") else value

        # Return the result
        return dictionary

    @staticmethod
    def process_nested_collection(value, should_ignore_null_values):
        if isinstance(value, list):
            return [ApiHelper.process_nested_collection(item, should_ignore_null_values) for item in value]

        if isinstance(value, dict):
            return {k: ApiHelper.process_nested_collection(v, should_ignore_null_values) for k, v in value.items()}

        return ApiHelper.to_dictionary(value, should_ignore_null_values) if hasattr(value, "_names") else value

    @staticmethod
    def apply_datetime_converter(value, datetime_converter_obj):
        if isinstance(value, list):
            return [ApiHelper.apply_datetime_converter(item, datetime_converter_obj) for item in value]

        if isinstance(value, dict):
            return {k: ApiHelper.apply_datetime_converter(v, datetime_converter_obj) for k, v in value.items()}

        if isinstance(value, datetime.datetime):
            return ApiHelper.when_defined(datetime_converter_obj, value)

        return value

    @staticmethod
    def when_defined(func, value):
        return func(value) if value else None

    @staticmethod
    def is_file_wrapper_instance(param):
        return isinstance(param, FileWrapper)

    @staticmethod
    def is_valid_type(value, type_callable, is_value_nullable=False, is_model_dict=False,
                      is_inner_model_dict=False):
        if value is None and is_value_nullable:
            return True

        if isinstance(value, list):
            return all(ApiHelper.is_valid_type(item, type_callable, is_value_nullable, is_model_dict,
                                               is_inner_model_dict) for item in value)
        elif isinstance(value, dict) and (not is_model_dict or is_inner_model_dict):
            return all(ApiHelper.is_valid_type(item, type_callable, is_value_nullable, is_model_dict)
                       for item in value.values())

        return value is not None and type_callable(value)

    @staticmethod
    def resolve_template_placeholders_using_json_pointer(placeholders, value, template):
        """Updates all placeholders in the given message template with provided value.

        Args:
            placeholders: The placeholders that need to be searched and replaced in the given template value.
            value: The dictionary containing the actual values to replace with.
            template: The template string containing placeholders.

        Returns:
            string: The resolved template value.
        """
        for placeholder in placeholders:
            extracted_value = ''

            if '#' in placeholder:
                # pick the 2nd chunk then remove the last character (i.e. `}`) of the string value
                node_pointer = placeholder.rsplit('#')[1].rstrip('}')
                try:
                    extracted_value = resolve_pointer(value, node_pointer) if node_pointer else ''
                    extracted_value = ApiHelper.json_serialize(extracted_value) \
                        if type(extracted_value) in [list, dict] else str(extracted_value)
                except JsonPointerException:
                    pass
            elif value is not None:
                extracted_value = ApiHelper.json_serialize(value)
            template = template.replace(placeholder, extracted_value)

        return template

    @staticmethod
    def resolve_template_placeholders(placeholders, values, template):
        """Updates all placeholders in the given message template with provided value.

                Args:
                    placeholders: The placeholders that need to be searched and replaced in the given template value.
                    values: The dictionary|string value which refers to the actual values to replace with.
                    template: The template string containing placeholders.

                Returns:
                    string: The resolved template value.
                """
        for placeholder in placeholders:
            if isinstance(values, abc.Mapping):
                # pick the last chunk then strip the last character (i.e. `}`) of the string value
                key = placeholder.rsplit('.', maxsplit=1)[-1].rstrip('}') if '.' in placeholder \
                    else placeholder.lstrip('{').rstrip('}')
                value_to_replace = str(values.get(key)) if values.get(key) else ''
                template = template.replace(placeholder, value_to_replace)
            else:
                values = str(values) if values is not None else ''
                template = template.replace(placeholder, values)

        return template

    @staticmethod
    def to_lower_case(list_of_string):
        """Converts all strings in a list to lowercase.

        Args:
            list_of_string (list): A list of strings to convert to lowercase.

        Returns:
            list: A new list containing the lowercase versions of the input strings.
                Returns None if the input list is None.

        Raises:
            TypeError: If the input is not a list.
        """
        if list_of_string is None:
            return None

        return list(map(lambda x: x.lower(), list_of_string))

    @staticmethod
    def get_additional_properties(dictionary, unboxing_function):
        """Extracts additional properties from the dictionary.

        Args:
            dictionary (dict): The dictionary to extract additional properties from.
            unboxing_function (callable): The deserializer to apply to each item in the dictionary.

        Returns:
            dict: A dictionary containing the additional properties and their values.
        """
        additional_properties = {}
        for key, value in dictionary.items():
            try:
                additional_properties[key] = unboxing_function(value)
            except Exception:
                pass

        return additional_properties


    class CustomDate(object):

        """ A base class for wrapper classes of datetime.

        This class contains methods which help in
        appropriate serialization of datetime objects.

        """

        def __init__(self, dtime, value=None):
            self.datetime = dtime
            if not value:
                self.value = self.from_datetime(dtime)
            else:
                self.value = value

        def __repr__(self):
            return str(self.value)

        def __getstate__(self):
            return self.value

        def __setstate__(self, state):  # pragma: no cover
            pass

    class HttpDateTime(CustomDate):

        """ A wrapper class for datetime to support HTTP date format."""

        @classmethod
        def from_datetime(cls, date_time):
            return eut.formatdate(timeval=mktime(date_time.timetuple()), localtime=False, usegmt=True)

        @classmethod
        def from_value(cls, value):
            dtime = datetime.datetime.fromtimestamp(eut.mktime_tz(eut.parsedate_tz(value)))
            return cls(dtime, value)

    class UnixDateTime(CustomDate):

        """ A wrapper class for datetime to support Unix date format."""

        @classmethod
        def from_datetime(cls, date_time):
            return calendar.timegm(date_time.utctimetuple())

        @classmethod
        def from_value(cls, value):
            dtime = datetime.datetime.utcfromtimestamp(float(value))
            return cls(dtime, int(value))

    class RFC3339DateTime(CustomDate):

        """ A wrapper class for datetime to support Rfc 3339 format."""

        @classmethod
        def from_datetime(cls, date_time):
            return date_time.isoformat()

        @classmethod
        def from_value(cls, value):
            dtime = dateutil.parser.parse(value)
            return cls(dtime, value)
