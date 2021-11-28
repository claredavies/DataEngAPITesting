import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Reading in file
    script_dir = os.path.dirname(__file__)
    rel_path = "test_cases_produced.csv"
    abs_file_path = os.path.join(script_dir, rel_path)

    df = pd.read_csv(abs_file_path)

    restAPIs = ['/petclinic/actuator', '/petclinic/error', '/petclinic/api/pets', '/petclinic/api/pettypes',
                '/petclinic/api/owners', '/petclinic/api/specialties', '/petclinic/api/users', '/petclinic/api/vets',
                '/petclinic/api/visits']

    general_request_uri = []
    for index, row in df.iterrows():
        found = False
        if (row['request_uri'] == '/petclinic'):
            general_request_uri.append('/petclinic')
            found = True
        if not found:
            for uri in restAPIs:
                if uri in row['request_uri']:
                    general_request_uri.append(uri)
                    pass
    df['general_request_uri'] = general_request_uri

    # Find number requests for each endpoint
    # add general_request_uri
    df1 = df.groupby('general_request_uri').size().reset_index(name='count')
    df1 = pd.DataFrame(df1)

    # Number of request by type for each endpoint
    df2 = df.groupby(['general_request_uri', 'request_type']).size().reset_index(name='request_type_count')
    df2 = pd.DataFrame(df2)

    # Number of request by type for each endpoint
    df3 = df.groupby(['general_request_uri', 'response_code']).size().reset_index(name='response_code_count')
    df3 = pd.DataFrame(df3)

    # Need to combine into 1 table where see for each endpoint the types of requests and responses
    df_general_request_request_type_response_type = pd.merge(df2, df3)
    script_dir = os.path.dirname(__file__)
    rel_path = "test_cases_analysis.csv"
    abs_file_path_csv = os.path.join(script_dir, rel_path)
    df_general_request_request_type_response_type.to_csv(abs_file_path_csv)

    plt.subplot(2, 3, 1)
    ax1 = pd.value_counts(df['general_request_uri']).plot.bar()

    plt.subplot(2, 3, 2)
    ax2 = pd.value_counts(df['response_code']).plot.bar()

    plt.subplot(2, 3, 3)
    ax3 = pd.value_counts(df['request_type']).plot.bar()

    ax1.title.set_text('General Request Count')
    ax2.title.set_text('Response Code Count')
    ax3.title.set_text('Request Type Count')

    plt.show()

if __name__ == "__main__":
    main()
