"""data.py
    data storage
    by Annika"""

import json

DATA_PATH = 'data.json'

def _loadJSON():
    """Loads the raw data from the json file

    Returns:
        dictionary -- the raw data
    """
    try:
        dataFile = open(DATA_PATH, 'r', encoding='utf-8')
        retval = json.load(dataFile)
        dataFile.close()
    except FileNotFoundError:
        retval = {}
    return retval

def get(variableName):
    """Gets the value of a variable that's stored in JSON

    Arguments:
        variableName {[string]} -- the name the variable was stored under

    Returns:
        [Any] -- the variable, or None if it doesn't exist
    """
    data = _loadJSON()
    if variableName in data.keys():
        return data[variableName]
    return None

def store(variableName, value):
    """Stores a variable to JSON

    Arguments:
        variableName {string} -- the name to save the value under
        value {Any} -- the value to save
    """
    data = _loadJSON()
    data[variableName] = value
    dataFile = open(DATA_PATH, 'w', encoding='utf-8')
    json.dump(data, dataFile)
    dataFile.close()
