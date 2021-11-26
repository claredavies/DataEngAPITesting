import os
import pandas as pd


def main():
    # Reading in file
    script_dir = os.path.dirname(__file__)
    rel_path = "test_cases_produced.csv"
    abs_file_path = os.path.join(script_dir, rel_path)

    df = pd.read_csv(abs_file_path)
    print(df.head())

    total_count = len(df.index)
    counts_unique = df.nunique()
    print("total_count ::  " + str(total_count))
    print("total unique requests:: " + str(counts_unique))

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
    print(df1['count'])
    df1 = pd.DataFrame(df1)

    # Number of request by type for each endpoint
    df2 = df.groupby(['general_request_uri', 'request_type']).size().reset_index(name='request_type_count')
    df2 = pd.DataFrame(df2)

    # Number of request by type for each endpoint
    df3 = df.groupby(['general_request_uri', 'response_code']).size().reset_index(name='response_code_count')
    df3 = pd.DataFrame(df3)

    # Need to combine into 1 table!
    df_final = pd.merge(df2, df3)

    print(df_final.head(20))

if __name__ == "__main__":
    main()
