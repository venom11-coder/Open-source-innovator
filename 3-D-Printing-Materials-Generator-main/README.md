#3-D-Printing-Materials-Generator

File 1: LoadInputs.py
Python program which contains the code to extract the appropriate inputs (natural and synthetic compounds). Currently, the natural compounds are limited to the chemicals found in the periodic table, and the synthetic/man-made compounds are limited to the CAS Common Chemistry API. 

File 2: CreateCombinations.py
Python program which contains the code to generate the materials consisting of two and three compounds. 

File 3: CompoundCombinationsList(5).txt
Sample output from a generator using an input size of five compounds. 

File 4: Case Study 1.py
Sample program to test the possible materials created from Glycerin, Water and Agar combination, corresponding to the experimental biomaterial data received from Materiom.  

File 5: InputData
Storage file where inputs retrieved using the LoadInputs.py program are stored in byte format. This is where the data is loaded from in the CreateCombinations.py program. 

File 6: Periodic_Table_of _Elements.csv
Source of natural chemicals and respective properties. 

File 7: Predictive Model - Elongation at Yield.ipynb
Regresison-based decision tree model to predict the elongation and yield property using the three % composition of water, agar, and glycerin as input variables. 

File 8: Predictive Model - Yield Strength.ipynb
Regression-based decision tree model to predict the yield strength property using the three % composition of water, agar, and glycerin as input variables. 

File 9: Predictive Model - Young Modulus.ipynb
Regression-based decision tree model to predict the young modulus property using the three % composition of water, agar, and glycerin as input variables. 

File 10: average_sample_data.csv 
Experimental data received from Materiom averaged for each combination variation. 
