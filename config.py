"""config.py
    loads configuration data from config.json
    by Annika"""

import json


CONFIG_PATH = 'config.json'
CONFIG_VARS = ['username', 'password', 'websocketURL', 'loglevel', 'sysops', 'broadcastRank',
    'addfactRank', 'hostgameRank', 'searchlogRank', 'manageRank', 'roomRanksInOrder', 'rooms', 'separator', 'modules',
    'commandCharacter', 'superheroAPIKey', 'pastebinAPIKey', 'logchat']

def loadConfig() -> list:
    """Loads configuration from CONFIG_PATH

    Returns:
        [list] -- the CONFIG_VARS as loaded from CONFIG_PATH
    """
    configData = json.load(open(CONFIG_PATH, 'r'))
    returnValue = []
    # make sure we're not missing anything
    for configItem in CONFIG_VARS:
        if configItem not in configData:
            # We can't use core.log() because config.loglevel doesn't exist yet
            print(f"E: {configItem} not found in config.json")
        else:
            returnValue.append(configData[configItem])
    return returnValue

# pylint: disable=unbalanced-tuple-unpacking
username, password, websocketURL, loglevel, sysops, broadcastRank, addfactRank, \
    hostgameRank, searchlogRank, manageRank, roomRanksInOrder, rooms, separator, modules, \
    commandCharacter, superheroAPIKey, pastebinAPIKey, logchat = loadConfig()
# the order of these needs to be the same as in CONFIG_VARS
