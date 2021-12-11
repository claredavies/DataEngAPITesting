Overall Instructions
1) Run the [server](https://github.com/claredavies/DataEngAPITesting/tree/master/RestAPI) on your local machine.

2) Generate the Test Cases for Restler using the instructions in the TestGenerationRestler folder (https://github.com/claredavies/DataEngAPITesting/blob/master/TestGenerationRestler/README.md)
3) The above should generate a text file containing info about the test cases generated e.g. network.testing.3180.1.txt
    and rename it to restler_output.txt 
4) Generate the Test Cases for Generative Model using the Instruction in the TestGenerationModel folder (https://github.com/claredavies/DataEngAPITesting/blob/master/TestGenerationModel/README.md)
5) The above should generate a text file containing info about the test cases generated. Make sure named generative_model_test_cases_produced.txt.
6) Follow Instructions in the ParseTestsAndAnalyse folder which will parse the restler_output.txt and generative_model_test_cases_produced.txt files and then         Analyse the results (https://github.com/claredavies/DataEngAPITesting/blob/master/ParseTestsAndAnalyse/README.md)
   
Note - there is also a AnomalyDetection folder which produces results but they are not yet very effective (WIP) (https://github.com/claredavies/DataEngAPITesting/blob/master/AnamolyDetection/README.md)



