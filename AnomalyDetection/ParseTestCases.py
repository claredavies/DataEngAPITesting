from datetime import datetime
from TestCase import TestCase
import pandas as pd

list_test_cases = []
time_sent = ""
time_received = ""
body = ""

with open('network.testing.3180.1.txt', "r") as fp:
    line_num = 0
    num_test_cases = 0
    for x in fp:
        line_num += 1
        if "Sending" in x:
            found = x.rstrip()
            splitted = found.split()
            time_sent = splitted[1]
            time_sent = time_sent[:-1]
            try:
                request_type = splitted[3]
                request_type = request_type[1:]
                request_uri = splitted[4]
                if 'application/json\\r\\nContent-Length' in x:
                    found = found.replace(request_uri,'')
                    first = found.find("{")
                    second = x.rfind("}")
                    if first != -1 and second != -1:
                        body = found[(first-1) + 1:second]
                        body = body.replace("\\n", "")
                        body = body.replace("\\r", "")
                        body = body.replace("'", "")
            except IndexError:
                print("invalid request:  \n")
        if "Received" in x:
            num_test_cases += 1
            found = x.rstrip()
            splitted = found.split()
            response_code = splitted[4]
            time_received = splitted[1]
            time_received = time_received[:-1]
            time_received = datetime.strptime(time_received, '%H:%M:%S.%f')
            time_sent = datetime.strptime(time_sent, '%H:%M:%S.%f')
            response_time = time_received - time_sent
            test_case = TestCase(request_type, request_uri, body, response_code, response_time.microseconds)
            list_test_cases.append(test_case)

df = pd.DataFrame([t.__dict__ for t in list_test_cases])
print(df.head())
df.to_csv('test_cases_produced.csv')

