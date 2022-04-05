class TestCase:
    def __init__(self, request_type=None, request_uri=None, request_body=None, response_code=None,
                 response_time_microseconds=None, valid_request=False):
        self.request_type = request_type
        self.request_uri = request_uri
        self.request_body = request_body
        self.response_code = response_code
        self.response_time_microseconds = response_time_microseconds
        self.valid_request = valid_request

    def _set_request_type(self, request_type):
        self._request_type = request_type

    def _set_request_uri(self, request_uri):
        self._request_uri = request_uri

    def _set_request_body(self, request_body):
        self._request_body = request_body

    def _set_response_code(self, response_code):
        self._response_code = response_code

    def _set_response_time_microseconds(self, response_time_microseconds):
        self._response_time_microseconds = response_time_microseconds

    def _set_valid_request(self, valid_request):
        self._valid_request = valid_request
