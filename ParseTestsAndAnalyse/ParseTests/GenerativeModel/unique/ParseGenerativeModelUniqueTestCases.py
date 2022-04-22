import os
from os import path
import pandas as pd
from ParseTestsAndAnalyse.ParseTests.Helper.GenerateResponses import GenerateResponses

basepath = path.dirname(__file__)
abs_file_path_folder = path.abspath(path.join(basepath, "..", "..", "..", "..", "TestGenerationModel/log/temp70"))
dirlist = [item for item in os.listdir(abs_file_path_folder) if os.path.isdir(os.path.join(abs_file_path_folder, item))]
print(dirlist)

for i in dirlist:
    abs_file_path_novel = path.abspath(path.join(abs_file_path_folder, i, "model_output_unique.txt"))
    list_test_cases = GenerateResponses.generateResponses(abs_file_path_novel)
    df_test_cases = pd.DataFrame([t.__dict__ for t in list_test_cases])

    script_dir = os.path.dirname(__file__)
    rel_path = "parsedTestCases/parsed_requests_generative_model_unique_produced_" + i + ".csv"
    abs_file_path_csv = os.path.join(script_dir, rel_path)
    df_test_cases.to_csv(abs_file_path_csv)
