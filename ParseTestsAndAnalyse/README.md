Instructions
1) Rename the output txt file from Restler as restler_output.txt. Then go to the ParseTests/Restler folder and paste in the restler_output.txt file. (Instruction for generating Restler file https://github.com/claredavies/DataEngAPITesting/tree/master/TestGenerationRestler)
2) Run the ParseTestCasesRestler.py file and it will produce a parsed file (don't move or touch as already in the right place)
3) Go to the ParseTests/GenerativeModel folder and either use the generative_model_test_cases_produced.txt already there or replace it with your own version
4) For parsing the test cases for the generative model the reponses from the RestAPIs need to be found which requires you running the RestAPIS locally 
   (instructions here https://github.com/claredavies/DataEngAPITesting/blob/master/RestAPI/readme.md)
5) Once running locally then run the ParseGenerativeModelTestCases.py which will produce a parsed file with responses (don't move or touch as already in the right place)
6) Then go into the Analysis folder and run the ParsedTestAnalysis.py file which should produce analysis files for both Restler and the Generative models as well as plots

![image](https://user-images.githubusercontent.com/91204973/144859084-8c475aed-46dd-46fc-b756-d3b019af2192.png)

