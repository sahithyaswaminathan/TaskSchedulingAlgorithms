Multiprocessor Systems Project

======================

DAG INPUT - TGFF package 
Link to download:  http://ziyang.eecs.umich.edu/~dickrp/tgff/

*Download the package
*The package must be compiled using the binary CPP compiler
*.tgffopt file is compiled using the inbulit commands and 3 output files are generated: .vcg, .eps and .tgff containing the DAG details 

======================

SOFTWARE REQUIRED

*Python(any version)

======================


INSTRUCTIONS TO RUN THE FILES:


1. Open the file by choosing the below algorithms 

2) If you are using Python 3.6, parameters must be configured in RUN environment using 'Configure per file'. 
The Parameters to be inputted include: 
a) FILE NAME: final.tgff 
b) no of processors: 3

======================


1) Ant Colony Optimisation Algorithm :  'ACO.py'


2) Ant Colony and Genetic Algorithm : 'GAACO.py'


3) Modified List scheduling Heuristic Algorithm: 'MLSH.py'


4) Modified List scheduling Heuristic Algorithm and Genetic Algorithm: 'GAMLSH.py'


=======================


If you are running from the terminal of Linux/MacOS or Pycharm:
Example to run the file:
>> python ACO.py final.tgff 3 
>> {file_name input_file no_of_prcessor}

=======================

Input TGFF File:
Run Only the .tgff suffix file 
The other .eps and .vcg file is used to view the DAG.
