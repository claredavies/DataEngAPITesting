from os import path
import pandas as pd
import matplotlib.pyplot as plt

def add_general_uri_column(test_dataframe, restAPIs):
    general_request_uri = []
    for index, row in test_dataframe.iterrows():
        found = False
        if (row['request_uri'] == '/petclinic'):
            general_request_uri.append('/petclinic')
            found = True
        if not found:
            for uri in restAPIs:
                if uri in row['request_uri']:
                    general_request_uri.append(uri)
                    pass
    test_dataframe['general_request_uri'] = general_request_uri

def main():
    # Reading in file
    basepath = path.dirname(__file__)
    # APITest/ParseTestsAndAnalyse/ParseTests/Restler/test_cases_produced_restler.csv
    abs_file_path_restler_test_cases = path.abspath(path.join(basepath, "..", "ParseTests/Restler"
                                                                                    "/test_cases_produced_restler.csv"))

    abs_file_path_generative_test_cases = path.abspath(path.join(basepath, "..", "ParseTests/GenerativeModel"
                                                                                       "/parsed_requests_generative_model_produced.csv"))

    df_restler_test_cases = pd.read_csv(abs_file_path_restler_test_cases)
    df_generative_test_cases = pd.read_csv(abs_file_path_generative_test_cases)


    restAPIs = ['/petclinic/actuator', '/petclinic/error', '/petclinic/api/pets', '/petclinic/api/pettypes',
                '/petclinic/api/owners', '/petclinic/api/specialties', '/petclinic/api/users', '/petclinic/api/vets',
                '/petclinic/api/visits','/petclinic/health','/petclinic/api/petid']

    add_general_uri_column(df_restler_test_cases, restAPIs)
    add_general_uri_column(df_generative_test_cases, restAPIs)

    # Number of request by type for each endpoint
    request_type_count_restler = df_restler_test_cases.groupby(['general_request_uri', 'request_type']).size().reset_index(
        name='request_type_count')
    request_type_count_restler = pd.DataFrame(request_type_count_restler)
    request_type_count_generative = df_generative_test_cases.groupby(['general_request_uri', 'request_type']).size().reset_index(
        name='request_type_count')
    request_type_count_generative = pd.DataFrame(request_type_count_generative)

    # Number of request by type for each endpoint
    response_code_count_restler = df_restler_test_cases.groupby(['general_request_uri', 'response_code']).size().reset_index(
        name='response_code_count')
    response_code_count_restler = pd.DataFrame(response_code_count_restler)
    response_code_count_generative = df_generative_test_cases.groupby(['general_request_uri', 'response_code']).size().reset_index(
        name='response_code_count')
    response_code_count_generative = pd.DataFrame(response_code_count_generative)

    # Need to combine into 1 table where see for each endpoint the types of requests and responses
    df_general_request_request_type_response_type_restler = pd.merge(request_type_count_restler, response_code_count_restler)
    rel_path_restler_test_cases = "test_cases_analysis_restler.csv"
    abs_file_path_csv_restler = path.abspath(path.join(basepath, rel_path_restler_test_cases))
    df_general_request_request_type_response_type_restler.to_csv(abs_file_path_csv_restler)

    df_general_request_request_type_response_type_generative = pd.merge(request_type_count_generative, response_code_count_generative)
    rel_path_generative_test_cases = "test_cases_analysis_generative.csv"
    abs_file_path_csv_generative = path.abspath(path.join(basepath, rel_path_generative_test_cases))
    df_general_request_request_type_response_type_generative.to_csv(abs_file_path_csv_generative)

    plt.subplot(3, 3, 1)
    ax1 = pd.value_counts(df_restler_test_cases['general_request_uri']).plot.bar()
    plt.subplot(3, 3, 7)
    ax4 = pd.value_counts(df_generative_test_cases['general_request_uri']).plot.bar()

    plt.subplot(3, 3, 2)
    ax2 = pd.value_counts(df_restler_test_cases['response_code']).plot.bar()
    plt.subplot(3, 3, 8)
    ax5 = pd.value_counts(df_generative_test_cases['response_code']).plot.bar()

    plt.subplot(3, 3, 3)
    ax3 = pd.value_counts(df_restler_test_cases['request_type']).plot.bar()
    plt.subplot(3, 3, 9)
    ax6 = pd.value_counts(df_generative_test_cases['request_type']).plot.bar()

    ax1.title.set_text('General Request Count Restler')
    ax4.title.set_text('General Request Count Generative')

    ax2.title.set_text('Response Code Count Restler')
    ax5.title.set_text('Response Code Count Generative')

    ax3.title.set_text('Request Type Count Restler')
    ax6.title.set_text('Request Type Count Generative')

    plt.show()


if __name__ == "__main__":
    main()
