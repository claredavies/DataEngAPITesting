class TestCase:
    def __init__(self, request_type, request_uri, request_body, response_code, response_time_microseconds):
        self.request_type = request_type
        self.request_uri = request_uri
        self.request_body = request_body
        self.response_code = response_code
        self.response_time_microseconds = response_time_microseconds
