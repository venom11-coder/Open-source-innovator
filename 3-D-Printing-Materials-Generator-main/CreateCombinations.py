import json
import csv
import time
import pickle
import itertools
from urllib.request import urlopen
start_time = time.time()

listOfCAS = []
listOfNaturalCompounds = []

#Object representing a man-made/synthetic compound with specific attributes
class SyntheticCompound:
    def __init__(self, name, inchi, molFormula, molMass):
        self.name = name
        self.inchi = inchi
        self.molFormula = molFormula
        self.molMass = molMass
        self.listOfProperties = []

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

#Object represeting the combined compound (material generated)
class CombinedCompound():
    def __init__(self, compound_number, list_of_compounds, list_of_weights):
        self.compound_number = compound_number
        self.listOfCompounds = list_of_compounds
        self.listOfWeights = list_of_weights
        self.functionalAgents = []

    def print_details(self):
        #print ('Compound Number: {} | Compounds: | {}{}  {}{}'.format(self.number,self.compounds[0],self.weights[0],self.compounds[1],self.weights[1]))
            print("Material Number: ", self.compound_number)
            num = 0;
            for item in self.listOfCompounds:
                print("Constituent ", num + 1,"\t", self.listOfCompounds[num].getName(), "\t", "Weight: ", self.listOfWeights[num], "%")
                num = num+1
            print()

# -----------------------------------CODE BEGINS----------------------------------------------

# Load objects (Load Pickle)
pickle_in = open("InputData", "rb")
newList = pickle.load(pickle_in)
numItems = 0;

#array holding new compounds
listOfCompoundCombinations = []
compoundNumber = 1;

#Combinations of 2
#Double nested loop to iterate through all synthetic+natural inputs
for i in range(0, 10, 1):
    for j in range(i+1, 10, 1):
        fraction1 = 99
        fraction2 = 1
        while fraction1 > 0:
            components = [newList[i], newList[j]]
            weights = [fraction1,fraction2]
            createdCompound = CombinedCompound(compoundNumber, components, weights)
            listOfCompoundCombinations.append(createdCompound)
            compoundNumber = compoundNumber + 1
            fraction1 = fraction1 - 1;
            fraction2 = fraction2 + 1;
print("Time to generate materials of two compounds\n --- %s seconds ---" % (time.time() - start_time))

#Combinations of 3
#Triple nested loop to iterate through all synthetic+natural inputs
for i in range(0, 10, 1):
    for j in range(i+1, 10, 1):
        for k in range(j+1, 10, 1):
            #generate all possible weight combinations (whole percentages)
            weightCombinations = [(a, b - a, 100 - b) for a, b in itertools.combinations(range(1, 100), 2)]
            for item in weightCombinations:
                components = [newList[i], newList[j], newList[k]]
                weights = [item[0],item[1],item[2]]
                createdCompound = CombinedCompound(compoundNumber, components, weights)
                listOfCompoundCombinations.append(createdCompound)
                compoundNumber = compoundNumber + 1
print("Time to generate materials of three compounds\n --- %s seconds ---" % (time.time() - start_time))

# Output compound combinations created into textfile
import sys
sys.stdout = open('CompoundCombinationsList(10).txt', 'w')
for item in listOfCompoundCombinations:
    item.print_details()


