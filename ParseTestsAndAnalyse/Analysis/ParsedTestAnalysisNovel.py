import os
from os import path
import pandas as pd
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join


def main():
    # Reading in file
    basepath = path.dirname(__file__)
    abs_file_path_folder = path.abspath(path.join(basepath, "..", "ParseTests/GenerativeModel/novel/parsedTestCases"))
    dirlist = [f for f in listdir(abs_file_path_folder) if isfile(join(abs_file_path_folder, f))]

    for i in dirlist:
        abs_file_path_novel = path.abspath(path.join(abs_file_path_folder, i))
        df_generative_test_cases = pd.read_csv(abs_file_path_novel)
        df_generative_test_cases.loc[
            df_generative_test_cases['request_type'].str.contains('OPTION'), 'request_type'] = 'OPTION'

        print("NAME of file: " + i)

        total_number_test_cases_generative_model = len(df_generative_test_cases.index)
        print("Total number of test cases generative model:   \n" + str(total_number_test_cases_generative_model))

        print("Counts for response codes generative model: \n" + str(pd.value_counts(df_generative_test_cases['response_code'])))
        print("Counts for request types generative model: \n" + str(pd.value_counts(df_generative_test_cases['request_type'])))

        print("Total number of test cases generative model:   \n" + str(total_number_test_cases_generative_model))
        no_invalid_cases = (df_generative_test_cases.response_code == 0).sum()

        no_valid_cases = total_number_test_cases_generative_model - no_invalid_cases
        print("Number of Novel Test Cases which are Valid Requests:  " + str(no_valid_cases.sum())
              + "   " + str(round(((no_valid_cases/total_number_test_cases_generative_model)*100),2)) + "%")

        no_invalid_cases = (df_generative_test_cases.response_code == 0).sum()
        print("Number of Novel Test Cases which are Invalid :  " + str(no_invalid_cases.sum())
              + "   " + str(round(((no_invalid_cases/total_number_test_cases_generative_model)*100),2)) + "%")

        no_passed_cases = (df_generative_test_cases.response_code == 200).sum()
        print("Number of Novel Test Cases Passed :  " + str(no_passed_cases.sum())
              + "   " + str(round(((no_passed_cases/total_number_test_cases_generative_model)*100),2)) + "%")

        no_failed_cases = (df_generative_test_cases.response_code == 404).sum() + (df_generative_test_cases.response_code == 500).sum()\
                          + (df_generative_test_cases.response_code == 400).sum()
        print("Number of Novel Test Cases Failed :  " + str(no_failed_cases.sum())
              + "   " + str(round(((no_failed_cases/total_number_test_cases_generative_model)*100),2)) + "%")


if __name__ == "__main__":
    main()
