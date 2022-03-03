class TestResponse:
    def __init__(self, request_type=None, response_code='', response_time='', response_error_msg='N/A',
                 response_error_class_name='N/A', response_connection='', response_content_length=None):
        self.request_type = request_type
        self.response_code = response_code
        self.response_time = response_time
        self.response_error_msg = response_error_msg
        self.response_error_class_name = response_error_class_name
        self.response_connection = response_connection
        self.response_content_length = response_content_length

    def _set_request_type(self, request_type):
        self._request_type = request_type

    def _set_response_code(self, response_code):
        self._response_code = response_code

    def _set_response_time(self, response_time):
        self._response_time = response_time

    def _set_response_error__msg(self, response_error_msg):
        self._response_error_msg = response_error_msg

    def _set_response_error_class_name(self, response_error_class_name):
        self._response_error_class_name = response_error_class_name

    def _set_response_connection(self, response_connection):
        self._response_connection = response_connection

    def _set_response_content_length(self, response_content_length):
        self._response_content_length = response_content_length
