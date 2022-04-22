from os import path
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Reading in file
    basepath = path.dirname(__file__)
    abs_file_path_folder = path.abspath(path.join(basepath, "..", "ParseTests/GenerativeModel/novel/parsedTestCases"))

    filename = "parsed_requests_generative_model_novel_produced_30min.csv"
    abs_file_path_novel = path.abspath(path.join(abs_file_path_folder, filename))
    df_generative_test_cases = pd.read_csv(abs_file_path_novel)

    df_generative_test_cases.loc[
        df_generative_test_cases['request_type'].str.contains('OPTION'), 'request_type'] = 'OPTION'

    print("NAME of file: " + filename)

    plt.figure()
    plt.subplot(2, 3, 1)
    ax1 = pd.value_counts(df_generative_test_cases['request_uri']).plot.bar()
    plt.subplot(2, 3, 2)
    ax2 = pd.value_counts(df_generative_test_cases['response_code']).plot.bar()
    plt.subplot(2, 3, 3)
    ax3 = pd.value_counts(df_generative_test_cases['request_type']).plot.bar()

    ax1.title.set_text('General Request Count Generative')
    ax2.title.set_text('Response Code Count Generative')
    ax3.title.set_text('Request Type Count Generative')

    plt.figure()
    plt.subplot(2, 2, 1)
    ax3 = pd.value_counts(df_generative_test_cases['request_type']).plot.pie()
    plt.subplot(2, 2, 2)
    ax4 = pd.value_counts(df_generative_test_cases['response_code']).plot.pie()
    ax3.title.set_text('General Request Count Generative')
    ax4.title.set_text('Response Code Count Generative')

    plt.show()

if __name__ == "__main__":
    main()
