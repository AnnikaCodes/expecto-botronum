#!/usr/bin/python3

import config
import re

################## core.py #####################
## core functionality of Expecto Botronum     ##
## by Annika                                  ##
################################################

######################
## Helper Functions ##
######################

def log(message):
    if config.loglevel > 2 or message[:2] == 'E:':
        # Errors are always logged and everything in debug mode is logged.
        print(message)
    elif message[:2] == 'W:' and config.loglevel >= 1:
        print(message)
    elif message[:2] == 'I:' and config.loglevel >= 2:
        print(message)

def toID(string):
    return re.sub('[^0-9a-zA-Z]+', '', string).lower()

################
## Room Class ##
################

class Room():
    def __init__(self, name):
        self.auth = self.updateAuth()
        self.id = toID(name)

    def updateAuth(self):
        log("W: Room.updateAuth() isn't implemented yet")
        return {'+': [], '%': [], '@': [], '#': []}

    def say(self, message):
        log("W: Room.say() isn't implemented yet")

    def leave(self):
        log("W: Room.leave() isn't implemented yet")
    
