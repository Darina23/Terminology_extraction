#######################################
TERMINOLOGY EXTRACTION
#######################################


A readme file for a command-line program implementation.



# Program Description #
-----------------------

With the help of statistical methods extract relevant for computational linguistics terminology from 
academic papers and compare the extracted terms with the golden standard.


# Installation - relevant information #
----------------------------

- Domain corpus texts (acl_texts) is located in the main directory together with 'src/', 'main.py' 'gold_terminology.txt', 'stopwords.txt' and 'Output/'.

- 'stopwords.txt' contains stopwords, needed for a program execution.

- 'Output/' contains txt files with alphas/thetas values and final terms (with their scores).

- 'src/' consists of separate classes, which can be directly executed. Their output is a class demonstration and unit tests results. 

- 'src/Output/' contains txt files, which are created by unit testing.

- 'src/test_folder/' is a toy directory with txt files needed for unit testing.

- 'src/toy_goldstandard.txt' is also needed for unit testing. 

- 'src/stopwords.txt' is also needed for unit testing.


# Program execution #
---------------------

-> In a terminal enter a path to the main directory, where main.py and other data is saved.

  #############   
###   Run:   ###
  ############     
	                        alpha(s)          theta(s)                    
                          
>>> python3 main.py acl_texts "0.2, 0.5, 0.7" "0.3, 0.6, 0.9" gold_terminology.txt. <<<


=> alphas are float-numbers, given in quotation marks, separated with ',' :  "0.7, 0.8"
=> thetas are float-numbers, given in quotation marks, separated with ',' :  "0.1, 1.0"


-> In the end of the execution precision and recall scores will be presented and txt-files with alpha/theta values and terms will be created in the directory Output/

......
