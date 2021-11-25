class TestResponse:
    def __init__(self, response_code='', response_time=''):
        self.response_code = response_code
        self.response_time = response_time

    def _set_response_code(self, response_code):
        self._response_code = response_code

    def _set_response_time(self, response_time):
        self._response_time = response_time
