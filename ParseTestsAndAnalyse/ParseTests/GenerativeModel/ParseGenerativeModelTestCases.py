import os
import pandas as pd
import requests

from ParseTestsAndAnalyse.ParseTests.Helper.ParsingMethods import ParsingMethods
from ParseTestsAndAnalyse.ParseTests.Helper.TestCase import TestCase

list_test_requests = ParsingMethods.readInTestCasesProducedGenerativeModel()

df_test_request = pd.DataFrame([t.__dict__ for t in list_test_requests])
print(df_test_request["request_body"].head())

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
    elif request_type == 'DELETE':
        response = requests.delete(api_url)
    elif request_type == 'HEAD':
        response = requests.head(api_url)
    try:
        response_code = response.status_code
        time_microseconds = response.elapsed.total_seconds()*1000000

        test_case = TestCase(request_type, row['request_uri'], row['request_body'],
                             response_code, time_microseconds)
        list_test_cases.append(test_case)
    except AttributeError:
        print(response)

df_test_cases = pd.DataFrame([t.__dict__ for t in list_test_cases])

script_dir = os.path.dirname(__file__)
rel_path = "parsed_requests_generative_model_produced.csv"
abs_file_path_csv = os.path.join(script_dir, rel_path)
df_test_cases.to_csv(abs_file_path_csv)
