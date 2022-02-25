import os
from ParseTestsAndAnalyse.ParseTests.Helper.TestRequest import TestRequest

class ParsingMethods:

    @staticmethod
    def readInTestCasesProducedGenerativeModel():
        list_test_requests = []

        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        script_dir = os.getcwd()

        rel_path_generative_model_cases = "GenerativeModel/generative_model_test_cases_produced.txt"
        abs_file_path_generative_model = os.path.join(script_dir, rel_path_generative_model_cases)

        # opening the file in read mode
        file = open(abs_file_path_generative_model, "r")
        for line in file:
            if line != "\n":
                found = line.rstrip()
                splitted = found.split()
                try:
                    request_type = splitted[1]
                    uri = splitted[2]
                    body = ''
                    first = found.find("{")
                    second = line.rfind("}")
                    if first != -1 and second != -1:
                        body = found[(first - 1) + 1:(second + 1)]
                        body = body.replace(" ", "")
                    test_request = TestRequest(request_type, uri, body, 0)
                    # Adding to list of test cases
                    list_test_requests.append(test_request)
                except IndexError:
                    print("handling non-valid line")
        return list_test_requests
