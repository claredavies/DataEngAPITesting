import os
import pandas as pd

from ParseTestsAndAnalyse.TestCase import TestCase
from ParseTestsAndAnalyse.TestRequest import TestRequest
import requests

list_test_requests = []

script_dir = os.path.dirname(__file__)
rel_path_generative_model_cases = "generative_model_test_cases_produced.txt"
abs_file_path_generative_model = os.path.join(script_dir, rel_path_generative_model_cases)

# opening the file in read mode
file = open(abs_file_path_generative_model, "r")
for line in file:
    if line != "\n":
        found = line.rstrip()
        splitted = found.split()
        request_type = splitted[1]
        uri = splitted[2]

        body = ''
        first = found.find("{")
        second = line.rfind("}")
        if first != -1 and second != -1:
            body = found[(first - 1) + 1:second]
            body = body.replace(" ", "")
        test_request = TestRequest(request_type, uri, body, 0)
        # Adding to list of test cases
        list_test_requests.append(test_request)


df_test_request = pd.DataFrame([t.__dict__ for t in list_test_requests])

list_test_cases = []
uri = "http://localhost:9966"
for index, row in df_test_request.iterrows():
    api_url = uri + row['request_uri']
    request_type = row['request_type']
    response = ''
    if request_type == 'GET':
        response = requests.get(api_url,row['request_body'])
    elif request_type == 'PUT':
        response = requests.put(api_url, row['request_body'])
    elif request_type == 'POST':
        response = requests.post(api_url, row['request_body'])
    # Can't have body' TypeError
    elif request_type == 'DELETE':
        response = requests.delete(api_url)
    # Can't have body' TypeError
    elif request_type == 'HEAD':
        response = requests.head(api_url)
    response_code = response.status_code
    time_microseconds = response.elapsed.total_seconds()*1000000

    test_case = TestCase(request_type, row['request_uri'], row['request_body'],
                         response_code, time_microseconds)

    list_test_cases.append(test_case)

df_test_cases = pd.DataFrame([t.__dict__ for t in list_test_cases])

script_dir = os.path.dirname(__file__)
rel_path = "parsed_requests_generative_model_produced.csv"
abs_file_path_csv = os.path.join(script_dir, rel_path)
df_test_cases.to_csv(abs_file_path_csv)
