from apimatic_core.exceptions.auth_validation_exception import AuthValidationException
from apimatic_core.http.request.http_request import HttpRequest
from apimatic_core.types.array_serialization_format import SerializationFormats
from apimatic_core.utilities.api_helper import ApiHelper


class RequestBuilder:

    @staticmethod
    def get_param_name(param_value):
        if isinstance(param_value, str):
            return None
        return param_value.name

    def __init__(
            self
    ):

        self._server = None
        self._path = None
        self._http_method = None
        self._template_params = {}
        self._header_params = {}
        self._query_params = {}
        self._form_params = {}
        self._additional_form_params = {}
        self._additional_query_params = {}
        self._multipart_params = []
        self._body_param = None
        self._body_serializer = None
        self._auth = None
        self._array_serialization_format = SerializationFormats.INDEXED
        self._xml_attributes = None

    def server(self, server):
        self._server = server
        return self

    def path(self, path):
        self._path = path
        return self

    def http_method(self, http_method):
        self._http_method = http_method
        return self

    def template_param(self, template_param):
        template_param.validate()
        self._template_params[template_param.get_key()] = {'value': template_param.get_value(),
                                                           'encode': template_param.need_to_encode()}
        return self

    def header_param(self, header_param):
        header_param.validate()
        self._header_params[header_param.get_key()] = header_param.get_value()
        return self

    def query_param(self, query_param):
        query_param.validate()
        self._query_params[query_param.get_key()] = query_param.get_value()
        return self

    def form_param(self, form_param):
        form_param.validate()
        self._form_params[form_param.get_key()] = form_param.get_value()
        return self

    def additional_form_params(self, additional_form_params):
        self._additional_form_params = additional_form_params
        return self

    def additional_query_params(self, additional_query_params):
        self._additional_query_params = additional_query_params
        return self

    def multipart_param(self, multipart_param):
        multipart_param.validate()
        self._multipart_params.append(multipart_param)
        return self

    def body_param(self, body_param):
        body_param.validate()
        if body_param.get_key():
            if not self._body_param:
                self._body_param = dict()
            self._body_param[body_param.get_key()] = body_param.get_value()
        else:
            self._body_param = body_param.get_value()
        return self

    def body_serializer(self, body_serializer):
        self._body_serializer = body_serializer
        return self

    def auth(self, auth):
        self._auth = auth
        return self

    def array_serialization_format(self, array_serialization_format):
        self._array_serialization_format = array_serialization_format
        return self

    def xml_attributes(self, xml_attributes):
        self._xml_attributes = xml_attributes
        return self

    def build(self, global_configuration):
        _url = self.process_url(global_configuration)

        _request_headers = self.process_request_headers(global_configuration)

        _request_body = self.process_body_params()

        _multipart_params = self.process_multipart_params()

        http_request = HttpRequest(http_method=self._http_method,
                                   query_url=_url,
                                   headers=_request_headers,
                                   parameters=_request_body,
                                   files=_multipart_params)

        self.apply_auth(global_configuration.get_auth_managers(), http_request)

        return http_request

    def process_url(self, global_configuration):
        _url = global_configuration.get_base_uri(self._server)
        _updated_url_with_template_params = self.get_updated_url_with_template_params()
        _url += _updated_url_with_template_params if _updated_url_with_template_params else self._path
        _url = self.get_updated_url_with_query_params(_url)
        return ApiHelper.clean_url(_url)

    def get_updated_url_with_template_params(self):
        return ApiHelper.append_url_with_template_parameters(self._path,
                                                             self._template_params) if self._template_params else None

    def get_updated_url_with_query_params(self, _query_builder):
        if self._additional_query_params:
            self.add_additional_query_params()
        return ApiHelper.append_url_with_query_parameters(_query_builder, self._query_params,
                                                          self._array_serialization_format)\
            if self._query_params else _query_builder

    def process_request_headers(self, global_configuration):
        request_headers = self._header_params
        global_headers = global_configuration.get_global_headers()
        additional_headers = global_configuration.get_additional_headers()

        if global_headers:
            prepared_headers = {key: str(value) if value is not None else value
                                for key, value in self._header_params.items()}
            request_headers = {**global_headers, **prepared_headers}

        if additional_headers:
            request_headers.update(additional_headers)

        return request_headers

    def process_body_params(self):
        if self._xml_attributes:
            return self.process_xml_parameters(self._body_serializer)
        elif self._form_params or self._additional_form_params:
            self.add_additional_form_params()
            return ApiHelper.form_encode_parameters(self._form_params, self._array_serialization_format)
        elif self._body_param is not None and self._body_serializer:
            return self._body_serializer(self.resolve_body_param())
        elif self._body_param is not None and not self._body_serializer:
            return self.resolve_body_param()

    def process_xml_parameters(self, body_serializer):
        if self._xml_attributes.get_array_item_name():
            return body_serializer(self._xml_attributes.get_value(),
                                   self._xml_attributes.get_root_element_name(),
                                   self._xml_attributes.get_array_item_name())

        return body_serializer(self._xml_attributes.get_value(), self._xml_attributes.get_root_element_name())

    def add_additional_form_params(self):
        if self._additional_form_params:
            for form_param in self._additional_form_params:
                self._form_params[form_param] = self._additional_form_params[form_param]

    def add_additional_query_params(self):
        for query_param in self._additional_query_params:
            self._query_params[query_param] = self._additional_query_params[query_param]

    def resolve_body_param(self):
        if ApiHelper.is_file_wrapper_instance(self._body_param):
            if self._body_param.content_type:
                self._header_params['content-type'] = self._body_param.content_type
            return self._body_param.file_stream

        return self._body_param

    def process_multipart_params(self):
        multipart_params = {}
        for multipart_param in self._multipart_params:
            param_value = multipart_param.get_value()
            if ApiHelper.is_file_wrapper_instance(param_value):
                file = param_value.file_stream
                multipart_params[multipart_param.get_key()] = (file.name, file, param_value.content_type)
            else:
                multipart_params[multipart_param.get_key()] = (self.get_param_name(param_value), param_value,
                                                               multipart_param.get_default_content_type())
        return multipart_params

    def apply_auth(self, auth_managers, http_request):
        if self._auth:
            if self._auth.with_auth_managers(auth_managers).is_valid():
                self._auth.apply(http_request)
            else:
                raise AuthValidationException(self._auth.error_message)
