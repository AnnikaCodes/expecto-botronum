#!/usr/bin/python3

import config
import re
import websocket
import requests
import json

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
    def __init__(self, name, connection):
        self.auth = []
        self.updateAuth()
        self.id = toID(name)
        self.connection = connection
        self.join()

    def updateAuth(self):
        '''Updates the auth list for the room. Returns the auth list'''
        log("W: Room.updateAuth() isn't implemented yet")
        self.auth = {'+': [], '%': [], '@': [], '*': [], '#': []}
        return self.auth

    def say(self, message):
        '''Sends the `message` to the room'''
        log("W: Room.say() isn't implemented yet")

    def leave(self):
        '''Leaves the room'''
        log("W: Room.leave() isn't implemented yet")

    def join(self):
        connection.send("|/j " + self.id)

    def usersWithRankGreaterThan(self, rank):
        '''returns a list of userids for the roomauth whose room rank is greater than the given `rank`'''
        userIDList = []
        for rank in config.roomRanksInOrder[config.roomRanksInOrder.index(rank):]:
            if rank in self.auth:
                userIDList.extend(self.auth[rank])
        return userIDList

################
## User Class ##
################

class User():
    def __init__(self, name):
        self.name = name
        self.id = toID(name)
        self.isAdmin = self.id in config.sysops

    def can(self, action, room):
        '''returns True if the user can do the action and False otherwise'''
        if action not in ['broadcast', 'addfact', 'hostgame', 'manage', 'admin']:
            log("E: User.can(): {action} isn't a valid action".format(action=action))
        return ((action == 'broadcast' and self.id in room.usersWithRankGreaterThan(config.broadcastRank)) or
            (action == 'addfact' and self.id in room.usersWithRankGreaterThan(config.addfactRank)) or
            (action == 'hostgame' and self.id in room.usersWithRankGreaterThan(config.hostgameRank)) or
            (action == 'manage' and self.id in room.usersWithRankGreaterThan(config.manageRank)) or
            self.isAdmin)

###################
## Message Class ##
###################

class Message():
    def __init__(self, raw):
        '''creates a Message object from the given `raw` websocket message'''
        log("W: Message() classes can't be properly instantiated yet, since __init__() logic isn't implemented yet")
        log("DEBUG: Message(): raw = {raw}".format(raw=raw))

        self.sender = None
        self.arguments = None
        self.room = None
        self.body = None
        self.time = None
        self.type = None
        self.challstr = None

        ### HACKY code to bootstrap for logins!
        if '|challstr|' in raw:
            self.challstr = raw.split('|challstr|')

######################
## Connection Class ##
######################

class Connection():
    def __init__(self):
        websocket.enableTrace(False)
        self.websocket = websocket.WebSocketApp(config.websocketURL,
            on_message = self.onMessage,
            on_error = self.onError,
            on_close = self.onClose, on_open = self.onOpen)
        self.roomList = []

    def onError(self, ws, error):
        log("E: Connection.onError(): websocket error: {error}".format(error = error))

    def onClose(self, ws):
        log("I: Connection.onClose(): websocket closed")

    def onOpen(self):
        log("I: Connection.onOpen(): websocket successfully opened")

    def onMessage(self, rawMessage):
        message = Message(rawMessage)
        if message.challstr:
            self.login(message.challstr)

    def login(self, challstr):
        '''logs in'''
        log("I: Connection.login(): logging in...")
        loginInfo = {'act': 'login', 'name': config.username, 'pass': config.password, 'challstr': challstr}
        loginResponse = requests.post('http://play.pokemonshowdown.com/action.php', data = loginInfo).content
        assertion = json.loads(loginResponse[1:].decode('utf-8'))['assertion']
        self.send('|/trn {name},0,{assertion}'.format(name = config.username, assertion = assertion))
        log("I: Connection.login(): joining rooms...")
        for room in config.rooms:
            self.roomList.append(Room(room, self))
        log("I: Connection.login(): rooms joined successfully")

    def send(self, message):
        '''sends message on the Connection'''
        self.websocket.send(message)

    def getRoomByID(self, id):
        '''Gets the Room object corresponding to the given ID'''
        objects = [room for room in self.roomList if room.id == id]
        if len(objects) == 1:
            return None
        elif len(objects) > 1:
            log("W: Connection.getRoomByID(): more than 1 Room object for room " + id)
        return objects[0]

    def getRoomByName(self, name):
        '''Gets the Room object for the room of the given name'''
        return self.getRoomByID(toID(name))

if __name__ == "__main__":
    connection = Connection()
    log("I: core.py: opening websocket...")
    connection.websocket.run_forever()
