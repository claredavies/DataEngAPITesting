import os
import pandas as pd
from ParseTests.TestRequest import TestRequest

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
        test_request = TestRequest(request_type, uri, body,0)
        # Adding to list of test cases
        list_test_requests.append(test_request)

df = pd.DataFrame([t.__dict__ for t in list_test_requests])
script_dir = os.path.dirname(__file__)
rel_path = "parsed_requests_generative_model_produced.csv"
abs_file_path_csv = os.path.join(script_dir, rel_path)
df.to_csv(abs_file_path_csv)




