class TestResponse:
    def __init__(self, response_code='', response_time='', response_msg='', response_class_name=''):
        self.response_code = response_code
        self.response_time = response_time
        self.response_msg = response_msg
        self._response_class_name = response_class_name

    def _set_response_code(self, response_code):
        self._response_code = response_code

    def _set_response_time(self, response_time):
        self._response_time = response_time

    def _set_response_msg(self, response_msg):
        self._response_msg = response_msg

    def _set_response_class_name(self, response_class_name):
        self._response_class_name = response_class_name
