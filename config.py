#!/usr/bin/python3

import json

################## config.py ###################
## loads configuration data from config.json  ##
## by Annika                                  ##
################################################

CONFIG_PATH = 'config.json'
CONFIG_VARS = ['username', 'password', 'websocketURL', 'loglevel', 'sysops', 'broadcastRank',
    'addfactRank', 'hostgameRank', 'manageRank', 'roomRanksInOrder', 'rooms', 'separator', 'modules',
    'commandCharacter']

def loadConfig():
    configData = json.load(open(CONFIG_PATH, 'r'))
    returnValue = []
    # make sure we're not missing anything
    for configItem in CONFIG_VARS:
        if configItem not in configData:
            # We can't use core.log because config.loglevel doesn't exist yet
            print("E: {item} not found in config.json".format(item = configItem))
        else:
            returnValue.append(configData[configItem])
    return returnValue

username, password, websocketURL, loglevel, sysops, broadcastRank, addfactRank, \
    hostgameRank, manageRank, roomRanksInOrder, rooms, separator, modules, \
    commandCharacter = loadConfig()
# the order of these needs to be the same as in CONFIG_VARS
