import os
from datetime import datetime
import pandas as pd

from TestCase import TestCase
from TestRequest import TestRequest
from TestResponse import TestResponse

list_test_cases = []


def extract_sending_request_info(current_line):
    found = current_line.rstrip()
    splitted = found.split()
    time_sent = splitted[1]
    time_sent = time_sent[:-1]
    body = ''
    try:
        request_type = splitted[3]
        request_type = request_type[1:]
        request_uri = splitted[4]
        if 'application/json\\r\\nContent-Length' in current_line:
            found = found.replace(request_uri, '')
            first = found.find("{")
            second = current_line.rfind("}")
            if first != -1 and second != -1:
                body = found[(first - 1) + 1:second]
                body = body.replace("\\n", "")
                body = body.replace("\\r", "")
                body = body.replace("'", "")
        current_test_request = TestRequest()
        current_test_request.request_type = request_type
        current_test_request.request_uri = request_uri
        current_test_request.request_body = body
        current_test_request.request_time = time_sent
        return current_test_request
    except IndexError:
        print("invalid request:  \n")
        return None


def extract_response_request_info(current_line):
    found = current_line.rstrip()
    splitted = found.split()
    response_code = splitted[4]
    response_time = splitted[1]
    response_time = response_time[:-1]
    current_test_response = TestResponse()
    current_test_response.request_code = response_code
    current_test_response.response_time = response_time
    return current_test_response


def get_reponse_time_microseconds(request_time_sent, response_time_received):
    time_received = datetime.strptime(response_time_received, '%H:%M:%S.%f')
    time_sent = datetime.strptime(request_time_sent, '%H:%M:%S.%f')
    response_time = time_received - time_sent
    return response_time.microseconds


def main():
    script_dir = os.path.dirname(__file__)
    rel_path = "restler_output.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, "r") as fp:
        test_request = TestRequest()
        test_response = TestResponse()
        for line in fp:
            if "Sending" in line:
                test_request = extract_sending_request_info(line)
            if "Received" in line:
                test_response = extract_response_request_info(line)
                time_microsecond = get_reponse_time_microseconds(test_request.request_time, test_response.response_time)
                test_case = TestCase(test_request.request_type, test_request.request_uri, test_request.request_body,
                                     test_response.response_code, time_microsecond)
                list_test_cases.append(test_case)

    df = pd.DataFrame([t.__dict__ for t in list_test_cases])
    print(df.head())
    df.to_csv('test_cases_produced.csv')


if __name__ == "__main__":
    main()
