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

    request_uri = df.request_uri.unique()

    df.request_uri.value_counts()

    df_grouped = df.groupby('request_uri')['request_type'].apply(lambda x: ' '.join(x.astype(str)))
    print(df_grouped)

    for key, value in df_grouped.items():
        words = value.split()
        word_remove_duplicates = " ".join(sorted(set(words), key=words.index))
        df_grouped[key] = word_remove_duplicates
        # removing as 14 of roughly same (injected_query_string)
        if 'petclinic/api/owners/owner' in key:
            del df_grouped[key]
        # removing as 14 of roughly same (injected_query_string)
        if '/petclinic/api/pets/pet' in key:
            del df_grouped[key]

    df_grouped['petclinic/api/owners/owner'] = 'PUT'
    df_grouped['petclinic/api/pets/pet'] = 'PUT'

    print(df_grouped)

if __name__ == "__main__":
    main()
