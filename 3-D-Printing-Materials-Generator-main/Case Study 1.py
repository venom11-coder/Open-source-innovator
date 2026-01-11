import itertools
import json
import csv
import ssl
from urllib.request import urlopen

ssl._create_default_https_context = ssl._create_unverified_context


class CAS_Object:
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
        self.molFormula = self.molFormula.encode('utf-8')
        self.molMass = self.molFormula.encode('utf-8')
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


class CAS_Properties:
    def __init__(self, propertyName, propertyDetails):
        self.name = propertyName
        self.details = propertyDetails


def CAS_object_creation(CASNumber):
    url = "https://commonchemistry.cas.org/api/detail?cas_rn="
    print(CASNumber)
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

        chemical_object = CAS_Object(name, inchi, molFor, molMass)

        for item in data['experimentalProperties']:
            propName = item['name']
            expProperty = item['property']
            property_object = CAS_Properties(propName, expProperty)
            chemical_object.listOfProperties.append(property_object)

        listOfCompounds.append(chemical_object)


class natural_compound_object:
    def __init__(self, name, atMass, type, density):
        self.name = name
        self.atMass = atMass
        self.type = type
        self.density = density

    def full_details(self):
        print(
            'Name: {}\nAtomic Mass: {}\nType: {}\nDensity: {}'.format(self.name, self.atMass, self.type, self.density))


class CombinedCompound():
    def __init__(self, compound_number, list_of_compounds, list_of_weights):
        self.compound_number = compound_number
        self.list_of_compounds = list_of_compounds
        self.list_of_weights = list_of_weights
        self.functional_agents = []

    def print_details(self):
        # print ('Compound Number: {} | Compounds: | {}{}  {}{}'.format(self.number,self.compounds[0],self.weights[0],self.compounds[1],self.weights[1]))
        print("Material Number: ", self.compound_number)
        num = 0;
        for item in self.list_of_compounds:
            print("Constituent ", num + 1, "\t", self.list_of_compounds[num].getName(), "\t", "Weight: ",
                  self.list_of_weights[num],"%")
            num = num + 1
        print()


# 1. Load basic elements from CAS Common Chemistry Registry
listOfMaterialsGenerated = []
listOfCAS = ["9002-18-0", "7732-18-5", "56-81-5"]
listOfCompounds = []

for item in listOfCAS:
    CAS_object_creation(str(item))

for item in listOfCompounds:
    item.full_details

# 2. Run combinations and create new Compounds
compoundNumber = 0;
# Combinations of 2

# makes combinations and new compounds
for i in range(0, 3, 1):
    for j in range(i + 1, 3, 1):
        fraction1 = 0.99
        fraction2 = 0.01
        while fraction1 > 0:
            components = [listOfCompounds[i], listOfCompounds[j]]
            weights = [fraction1, fraction2]
            createdCompound = CombinedCompound(compoundNumber, components, weights)
            listOfMaterialsGenerated.append(createdCompound)
            compoundNumber = compoundNumber + 1
            fraction1 = fraction1 - 0.01;
            fraction2 = fraction2 + 0.01;

# #Combinations of 3
for i in range(0, 3, 1):
    for j in range(i + 1, 3, 1):
        for k in range(j + 1, 3, 1):
            weightCombinations = [(a, b - a, 100 - b) for a, b in itertools.combinations(range(1, 100), 2)]
            for item in weightCombinations:
                components = [listOfCompounds[i], listOfCompounds[j], listOfCompounds[k]]
                weights = [item[0], item[1], item[2]]
                createdCompound = CombinedCompound(compoundNumber, components, weights)
                listOfMaterialsGenerated.append(createdCompound)
                compoundNumber = compoundNumber + 1

# Print Compound Combinations Created
for item in listOfMaterialsGenerated:
    item.print_details()

# 3. Update properties based on spreadsheet


# 4. Retrieve based on required properties (demonstration of use case 2)
