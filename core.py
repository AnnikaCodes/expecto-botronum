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
        '''Updates the auth list for the room. Returns the auth list'''
        log("W: Room.updateAuth() isn't implemented yet")
        self.auth = {'+': [], '%': [], '@': [], '*', '#': []}
        return self.auth

    def say(self, message):
        '''Sends the `message` to the room'''
        log("W: Room.say() isn't implemented yet")

    def leave(self):
        '''Leaves the room'''
        log("W: Room.leave() isn't implemented yet")

    def usersWithRankGreaterThan(self, rank):
        '''returns a list of userids for the roomauth whose room rank is greater than the given `rank`'''
        userIDList = []
        for rank in config.roomRanksInOrder[config.roomRanksInOrder.index(rank):]:
            if rank in self.auth:
                userIDList.extend(self.auth[rank])
        return userIDList

class User():
    def __init__(self, name):
        self.name = name
        self.id = toID(name)
        self.isAdmin = self.id in config.sysops

    def can(self, action, room):
        '''returns True if the user can do the action and False otherwise'''
        if action not in ['broadcast', 'addfact', 'hostgame', 'manage', 'admin']:
            log("E: User.can(): {action} isn't a valid action".format(action=action))
        return ((action === 'broadcast' and self.id in room.usersWithRankGreaterThan(config.broadcastRank)) or
            (action === 'addfact' and self.id in room.usersWithRankGreaterThan(config.addfactRank)) or
            (action === 'hostgame' and self.id in room.usersWithRankGreaterThan(config.hostgameRank)) or
            (action === 'manage' and self.id in room.usersWithRankGreaterThan(config.manageRank)) or
            self.isAdmin)
    
