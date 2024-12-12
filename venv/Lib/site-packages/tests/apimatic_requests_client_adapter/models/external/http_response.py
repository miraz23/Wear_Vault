# -*- coding: utf-8 -*-


class HttpResponse(object):

    def __init__(self,
                 status_code,
                 reason,
                 headers,
                 text,
                 content):
        self.status_code = status_code
        self.reason = reason
        self.headers = headers
        self.text = text
        self.content = content
