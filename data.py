##### data.py ####
## data storage ##
## by Annika    ##
##################

import json

DATA_PATH = 'data.json'

def __loadJSON():
    """Loads the raw data from the json file

    Returns:
        dictionary -- the raw data
    """    
    f = open(DATA_PATH, 'r')
    return json.load(f)

def get(variableName):
    """Gets the value of a variable that's stored in JSON

    Arguments:
        variableName {[string]} -- the name the variable was stored under

    Returns:
        [Any] -- the variable
    """    
    data = __loadJSON()
    if variableName in data.keys():
        return data[variableName]
    return None

def store(variableName, value):
    """Stores a variable to JSON

    Arguments:
        variableName {string} -- the name to save the value under
        value {Any} -- the value to save
    """    
    data = __loadJSON()
    data[variableName] = value
    f = open(DATA_PATH, 'w')
    json.dump(data, f)