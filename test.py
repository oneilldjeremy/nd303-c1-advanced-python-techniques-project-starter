from extract import load_neos, load_approaches
from database import NEODatabase
from filters import valid_attribute, limit
import operator
import math
import datetime
import operator

neos = load_neos('./tests/test-neos-2020.csv')
cads = load_approaches('./tests/test-cad-2020.json')

neo_database =  NEODatabase(neos, cads)

result = neo_database.get_neo_by_designation('1865')

#print(result)


#print(get_attribute(an_approach, operator.eq, value, attribute))

#print(neo_1036.approaches)

#print(neo_database.get_neo_by_name('Ganymed'))