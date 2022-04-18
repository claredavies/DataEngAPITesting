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
        abs_file_path_novel = path.abspath(path.join(abs_file_path_folder,i))
        df_generative_test_cases = pd.read_csv(abs_file_path_novel)
        df_generative_test_cases.loc[df_generative_test_cases['request_type'].str.contains('OPTION'), 'request_type'] = 'OPTION'

        print("NAME of file: " + i)
        # plt.figure()
        # plt.subplot(2, 3, 1)
        # ax1 = pd.value_counts(df_generative_test_cases['request_uri']).plot.bar()
        # plt.subplot(2, 3, 2)
        # ax2 = pd.value_counts(df_generative_test_cases['response_code']).plot.bar()
        # plt.subplot(2, 3, 3)
        # ax3 = pd.value_counts(df_generative_test_cases['request_type']).plot.bar()
        #
        # ax1.title.set_text('General Request Count Generative')
        # ax2.title.set_text('Response Code Count Generative')
        # ax3.title.set_text('Request Type Count Generative')
        #
        # plt.figure()
        # plt.subplot(2, 2, 1)
        # ax3 = pd.value_counts(df_generative_test_cases['request_type']).plot.pie()
        # plt.subplot(2, 2, 2)
        # ax4 = pd.value_counts(df_generative_test_cases['response_code']).plot.pie()
        # ax3.title.set_text('General Request Count Generative')
        # ax4.title.set_text('Response Code Count Generative')

        total_number_test_cases_generative_model = len(df_generative_test_cases.index)
        print("Total number of test cases generative model:   " + str(total_number_test_cases_generative_model))
        df_generative_unique = df_generative_test_cases.drop_duplicates(
            subset=['request_uri', 'request_type', 'request_body'])
        total_number_unique_test_cases_generative = len(df_generative_unique.index)
        print("Total unique test cases generative model:   " + str(total_number_unique_test_cases_generative))
        print("Counts for response codes generative model: ")
        print(pd.value_counts(df_generative_test_cases['response_code']))
        print("Counts for request types generative model: ")
        print(pd.value_counts(df_generative_test_cases['request_type']))
        print("Average response time generative model:  " + str((sum(
            df_generative_test_cases['response_time_microseconds']) / total_number_test_cases_generative_model) / 1000000))
        print("Uniqueness % (Number of unique tests / Total tests generated) generative model:  " + str(
            (total_number_unique_test_cases_generative / total_number_test_cases_generative_model) * 100))

        # plt.show()

if __name__ == "__main__":
    main()
