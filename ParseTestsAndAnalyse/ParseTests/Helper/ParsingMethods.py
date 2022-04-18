import os
from ParseTestsAndAnalyse.ParseTests.Helper.TestRequest import TestRequest


class ParsingMethods:

    @staticmethod
    def readInTestCasesProducedGenerativeModel(abs_file_path_generative_model):
        list_test_requests = []

        # opening the file in read mode
        file = open(abs_file_path_generative_model, "r")
        for line in file:
            if line != "\n":
                found = line.rstrip()
                splitted = found.split()
                test_request = TestRequest()
                try:
                    test_request.request_type = splitted[1]
                    if len(splitted) == 2:
                        test_request.request_uri = ''
                        test_request.request_body = ''
                    else:
                        if '/' in splitted[2]:
                            test_request.request_uri = splitted[2]
                        else:
                            test_request.request_uri = ''
                        test_request.request_body = ''
                        first = found.find("{")
                        second = line.rfind("}")
                        if first != -1 and second != -1:
                            test_request.request_body = found[(first - 1) + 1:(second + 1)]
                            test_request.request_body = test_request.request_body.replace(" ", "")
                        # Adding to list of test cases
                    list_test_requests.append(test_request)
                except IndexError:
                    print("Unable to handle following line: " + str(splitted))

        return list_test_requests
