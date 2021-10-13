# AWS Data Engineering/DevOps project

### Table of Contents

### General Description 

The main goal of this project is to create the infrastructure in AWS Cloud for
Automated Processing of .txt files, with using an AWS Lambda, Injected Python Script and S3 Bucket for Storing
and Inputting the data


### Python Scripts

In this repository you can find two versions of the same script. First "script.py" - for executing in the local environment, Second "script_optimized_for_lambda.py" - specially optimized for running
in AWS Lambda environment. Documentation on every part of the script can be find "commented" in the files themselves. The only library which was used for creating scripts is injected python library "csv"
for parsing the input files, other operations were hard-coded using the core Python language. The main approach for solving the problem was to extract the unique occupations/states from the Input File then 
for each of occupations/states extract the amount of certified applications and at the same time the overall amount of certified applications in order to generate the percentage, finally sort the whole 
list of occupations/states firstly by amount of certified applications and then extract data points with the same amount of applications, sort them alphabetically and add  

 
Explanation of methods present in a script:
* find_index()

### Infrastructure
