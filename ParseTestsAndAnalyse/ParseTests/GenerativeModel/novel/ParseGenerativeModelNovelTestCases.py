import os
from os import path
import pandas as pd
import requests
from requests.exceptions import InvalidURL

from ParseTestsAndAnalyse.ParseTests.Helper.ParsingMethods import ParsingMethods
from ParseTestsAndAnalyse.ParseTests.Helper.TestCase import TestCase

basepath = path.dirname(__file__)
abs_file_path_folder = path.abspath(path.join(basepath, "..", "..", "..", "..", "TestGenerationModel/log/temp70"))
dirlist = [item for item in os.listdir(abs_file_path_folder) if os.path.isdir(os.path.join(abs_file_path_folder, item))]
print(dirlist)

for i in dirlist:
    abs_file_path_novel = path.abspath(path.join(abs_file_path_folder, i, "model_output_novel_t7_le5000.txt"))
    list_test_requests = ParsingMethods.readInTestCasesProducedGenerativeModel(abs_file_path_novel)

    df_test_request = pd.DataFrame([t.__dict__ for t in list_test_requests])
    print(df_test_request["request_body"].head())

    list_test_cases = []
    uri = "http://localhost:9966"
    count_invalid = 0
    count_valid = 0
    for index, row in df_test_request.iterrows():
        api_url = uri + row['request_uri']
        request_type = row['request_type']
        response = ''
        try:
            if request_type == 'GET':
                response = requests.get(api_url, row['request_body'])
            elif request_type == 'PUT':
                response = requests.put(api_url, row['request_body'])
            elif request_type == 'POST':
                response = requests.post(api_url, row['request_body'])
            elif request_type == 'DELETE':
                response = requests.delete(api_url)
            elif request_type == 'HEAD':
                response = requests.head(api_url)
            elif request_type == 'OPTION':
                print("option body:   " + row['request_body'])
                response = requests.options(api_url)
            elif request_type == 'PATCH':
                response = requests.patch(api_url, row['request_body'])
            response_code = response.status_code
            time_microseconds = response.elapsed.total_seconds() * 1000000

            test_case = TestCase(request_type, row['request_uri'], row['request_body'],
                                 response_code, time_microseconds, True)
            count_valid = count_valid + 1
            list_test_cases.append(test_case)
        except InvalidURL:
            print("InvalidURL:  " + row + "\n")
            count_invalid = count_invalid + 1
            test_case = TestCase(request_type, row['request_uri'], row['request_body'],
                                 0, 0, False)
            list_test_cases.append(test_case)
            continue
        except AttributeError:
            print("attribute error:  " + row + "\n")
            count_invalid = count_invalid + 1
            test_case = TestCase(request_type, row['request_uri'], row['request_body'],
                                 0, 0, False)
            list_test_cases.append(test_case)

    df_test_cases = pd.DataFrame([t.__dict__ for t in list_test_cases])

    print("invalid test cases: " + str(count_invalid))
    print("invalid test cases: " + str(count_valid))
    print("total no of test cases: " + str(count_valid + count_invalid))

    script_dir = os.path.dirname(__file__)
    rel_path = "parsedTestCases/parsed_requests_generative_model_novel_produced_" + i + ".csv"
    abs_file_path_csv = os.path.join(script_dir, rel_path)
    df_test_cases.to_csv(abs_file_path_csv)
