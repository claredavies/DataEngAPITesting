## Note

`GPT_Model.ipynb` is easily runnable on Google Colab. Make sure to run it on the GPU.

You just need to import `src` folder and `test_cases_produced.csv`

This notebook produced several files (the name of the files may be different based on what you choose during running):

### 1. RESTler_unique_output.txt
The input file (`test_cases_produced.csv`) may contain duplicate requests. Also, it has several features. This script preprocesses the input file and makes it pure.

### 2. model_output_raw.txt
This is the output of our model. In this file, `END_OF_SAMPLE` shows where one sample ends.

### 3. model_output_unique.txt
The previous output file contains duplicate requests, and it should also be processed to eliminate the `END_OF_SAMPLE` line and one before.
The reason why we eliminate the line before `END_OF_SAMPLE` is that it may be incomplete due to the length of the generated sequence.

### 4. model_output_novel_t7_le5000.txt
The previous file is compared with the initial input dataset, and novel data is extracted.
