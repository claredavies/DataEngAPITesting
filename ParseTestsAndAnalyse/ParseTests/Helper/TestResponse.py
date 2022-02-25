class TestResponse:
    def __init__(self, response_code='', response_time='', response_msg=None, response_headers=None):
        self.response_code = response_code
        self.response_time = response_time
        self.response_msg = response_msg
        self._response_headers = response_headers

    def _set_response_code(self, response_code):
        self._response_code = response_code

    def _set_response_time(self, response_time):
        self._response_time = response_time

    def _set_response_msg(self, response_msg):
        self._response_msg = response_msg

    def _set_response_headers(self, response_headers):
        self._response_headers = response_headers
