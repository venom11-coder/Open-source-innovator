import json
import csv
import time
import pickle
from urllib.request import urlopen
import requests as requests
from bs4 import BeautifulSoup
import pandas as pd
import ssl
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import JSONResponse

app=FastAPI()

ssl._create_default_https_context = ssl._create_unverified_context
start_time = time.time()
listOfCAS = []
listOfNaturalCompounds = []
errors = 0

#Object representing a man-made/synthetic compound with specific attributes
# 
class SyntheticCompound:
    def __init__(self, name, inchi, molFormula, molMass):
        self.name = name
        self.inchi = inchi
        self.molFormula = molFormula
        self.molMass = molMass
        self.listOfProperties = []

    # prints the list
    def print_list(self):
        for item in self.listOfProperties:
            print("Experimental Property: " + item.name + " | " + item.details)
    
    def full_details(self):
        if not isinstance(self.molFormula, bytes):
            self.molFormula = self.molFormula.encode('utf-8')
        if not isinstance(self.molMass, bytes):
            self.molMass = self.molMass.encode('utf-8')
        try:
            print('Name: {}\nInchi: {}\nMolecular Formula: {}\nMolecular Mass: {}'.format(self.name, self.inchi,
                                                                                          self.molFormula,
                                                                                          self.molMass))
        except Exception:
            print("Encoding Error")
        else:
            print('Name: {}\nInchi: {}\nMolecular Formula: {}\nMolecular Mass: {}'.format(self.name, self.inchi,
                                                                                          self.molFormula,
                                                                                          self.molMass))
            self.print_list()

    def getName(self):
        return self.name

#Object representing the experimental properties pulled from the Common Chemistry API
#Prints the properties received from Common Chemistry API
class CAS_Properties:
    def __init__(self, propertyName, propertyDetails):
        self.name = propertyName
        self.details = propertyDetails

#Method to create SyntheticCompound Objects using Common Chemistry API
def CAS_object_creation(CASNumber):
    url = "https://commonchemistry.cas.org/api/detail?cas_rn="
    final_url = url + CASNumber
    print(final_url)
    try:
        returned = urlopen(final_url)
    except Exception:
        print(final_url)
        print("Error")
    else:
        data = json.load(returned)
        name = data['name']
        inchi = data['inchi']
        molFor = data['molecularFormula'].replace('</sub>', '').replace('<sub>', '')
        molMass = data['molecularMass']
        chemical_object = SyntheticCompound(name, inchi, molFor, molMass)

        for item in data['experimentalProperties']:
            propName = item['name']
            expProperty = item['property']
            property_object = CAS_Properties(propName, expProperty)
            chemical_object.listOfProperties.append(property_object)

        listOfCAS.append(chemical_object)

#Object representing a natural compound with a few common attributes
class NaturalCompound:
    def __init__(self, name, atMass, type, density):
        self.name = name
        self.atMass = atMass
        self.type = type
        self.density = density

    def full_details(self):
        print(
            'Name: {}\nAtomic Mass: {}\nType: {}\nDensity: {}'.format(self.name, self.atMass, self.type, self.density))

#Method to create NaturalCompound objects by iterating through the periodic table
def natural_compounds_creation():
    with open('Periodic_Table_of _Elements.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for line in reader:
            name = line[1]
            mass = line[3]
            type = line[15]
            density = line[19]
            periodic_compound = NaturalCompound(name, mass, type, density)
            listOfNaturalCompounds.append(periodic_compound)

# -----------------------------------CODE BEGINS----------------------------------------------
#CAS REGISTRY INITIALIZATION

with open('CAS_Sample_List.csv') as file:
    reader = csv.reader(file)
    next(reader)
    for line in reader:
        CAS_number = line[1]
        CAS_object_creation(CAS_number)

#Currently, CAS numbers are obtained from table in Wikipedia
wiki_url = "https://en.wikipedia.org/wiki/List_of_CAS_numbers_by_chemical_compound#External_links"
table_class = "wikitable"
response = requests.get(wiki_url)
soup = BeautifulSoup(response.text, 'html.parser')
compound_directories = soup.findAll('table', attrs={'class': table_class})
CAS_number_list = []

#create list of CAS numbers from Wiki
for table in compound_directories:
    formatted_compound_table = pd.read_html(str(table), header=0)[0]
    CAS_number_list.append(formatted_compound_table['CAS number'].tolist())
#create SyntheticCompound for each CAS number
for list in CAS_number_list:
    for number in list:
        if (type(number) != float):
            CAS_object_creation(number)

#PERIODIC TABLE ELEMENTS INITIALIZATION
#use helper method to create NaturalCompound objects
natural_compounds_creation()

for item in listOfNaturalCompounds:
    item.full_details()
    print

for item in listOfCAS:
    item.full_details()
    print

#Save objects (Write Pickle) so it can be accessed in 'CreateCombinations.py' file
pickle_out = open("InputData", "wb")
pickle.dump(listOfCAS, pickle_out)
pickle_out.close()

print("DONE")


