class TestRequest:
    def __init__(self, request_type='', request_uri='', request_body='', request_time=''):
        self.request_type = request_type
        self.request_uri = request_uri
        self.request_body = request_body
        self.request_time = request_time

    def _set_request_type(self, request_type):
        self._request_type = request_type

    def _set_request_uri(self, request_uri):
        self._request_uri = request_uri

    def _set_request_body(self, request_body):
        self._request_body = request_body

    def _set_request_time(self, request_time):
        self._request_time = request_time
