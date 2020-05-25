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
        self.id = toID(name)
        self.auth = {}
        self.connection = connection
        self.join()

    def updateAuth(self, authDict):
        '''Updates the auth list for the room based on the given auth dict'''
        for key in authDict.keys():
            if self.auth[key]:
                self.auth[key] += authDict[key]
            else:
                self.auth[key] = authDict[key]

    def say(self, message):
        '''Sends the `message` to the room'''
        self.connection.send(self.id + "|" + message)

    def leave(self):
        '''Leaves the room'''
        log("W: Room.leave() isn't implemented yet")

    def join(self):
        self.connection.send("|/j " + self.id)
        self.say('/roomauth')

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
    def __init__(self, name, connection):
        self.name = name
        self.id = toID(name)
        self.isAdmin = self.id in config.sysops
        self.connection = connection

    def can(self, action, room):
        '''returns True if the user can do the action and False otherwise'''
        if action not in ['broadcast', 'addfact', 'hostgame', 'manage', 'admin']:
            log("E: User.can(): {action} isn't a valid action".format(action=action))
        return ((action == 'broadcast' and self.id in room.usersWithRankGreaterThan(config.broadcastRank)) or
            (action == 'addfact' and self.id in room.usersWithRankGreaterThan(config.addfactRank)) or
            (action == 'hostgame' and self.id in room.usersWithRankGreaterThan(config.hostgameRank)) or
            (action == 'manage' and self.id in room.usersWithRankGreaterThan(config.manageRank)) or
            self.isAdmin)

    def PM(self, message):
        '''PMs the user the given message'''
        self.connection.whisper(self.id, message)

###################
## Message Class ##
###################

class Message():
    def __init__(self, raw, connection):
        '''creates a Message object from the given `raw` websocket message'''
        self.sender = None
        self.arguments = None
        self.room = None
        self.body = None
        self.time = None
        self.type = None
        self.challstr = None
        self.connection = connection

        split = raw.split("|")
        self.type = split[1]

        ### Note: there's a lot of reused / copy+paste logic here
        ### It might be worth looking into a better way to format this
        ### tbh all of Message() is kludgy
        if self.type == 'challstr':
            self.challstr = "|".join(split[2:])
        elif self.type in ['c:', 'c', 'chat']:
            hasTimestamp = (self.type == 'c:')
            self.type = 'chat'
            self.room = connection.getRoomByID(split[0].strip('>').strip('\n'))

            currentSlice = 2
            if hasTimestamp:
                self.time = split[currentSlice]
                currentSlice += 1

            username = split[currentSlice].strip()
            currentSlice += 1
            if username[0] in config.roomRanksInOrder:
                rank = username[0]
                username = username[1:]
                self.room.updateAuth({rank: username})
            self.sender = User(username, self.connection) 
            self.body = "|".join(split[currentSlice:]).strip('\n')
        elif self.type in ['J', 'j', 'join']:
            self.type = 'join'
            self.room = connection.getRoomByID(split[0].strip('>').strip('\n'))
            self.sender = User(split[2], self.connection)
        elif self.type == 'pm':
            self.sender = User(split[2], self.connection)
            self.body = "|".join(split[4:]).strip('\n')
        elif self.type == 'popup':
            useridsFromPopup = lambda popupData : [userid.strip('*') for userid in popupData.split(", ")] 
            if split[2] == 'Room Owners (#):':
                roomName = split[-1].split(" is a ", 1)[0]
                try:
                    room = self.connection.getRoomByName(roomName)
                except Exception as e:
                    log("E: Message(): cannot parse auth popup for room {room}: {err}".format(room = roomName, err = str(e)))
                
                owners = bots = mods = drivers = voices = []
                for i in range(len(split)):
                    if split[i] == 'Room Owners (#):':
                        owners = useridsFromPopup(split[i + 2])
                    elif split[i] == 'Bots (*):':
                        bots = useridsFromPopup(split[i + 2])
                    elif split[i] == 'Moderators (@):':
                        mods = useridsFromPopup(split[i + 2])
                    elif split[i] == 'Drivers (%):':
                        drivers = useridsFromPopup(split[i + 2])
                    elif split[i] == 'Voices (+):':
                        voices = useridsFromPopup(split[i + 2])
                
                authList = {'#': owners, '*': bots, '@': mods, '%': drivers, '+': voices}
                room.updateAuth(authList)
        else:
            log("DEBUG: Message() of unknown type {type}: {raw}".format(type = self.type, raw = raw))
        if self.body:
            self.arguments = self.body.split(config.separator)

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
        self.commands = {}
        for module in config.modules:
            self.commands.update(module.commands)
            # Note: if multiple modules have the same command then the later module will overwrite the earlier.
        log("I: Connection(): Loaded the following commands: " + ", ".join(self.commands.keys()))

    def onError(self, ws, error):
        log("E: Connection.onError(): websocket error: {error}".format(error = error))

    def onClose(self, ws):
        log("I: Connection.onClose(): websocket closed")

    def onOpen(self):
        log("I: Connection.onOpen(): websocket successfully opened")

    def onMessage(self, rawMessage):
        message = Message(rawMessage, self)
        if message.challstr:
            self.login(message.challstr)
        elif message.type in ['chat', 'pm'] and message.body[0] == config.commandCharacter:
            potentialCommand = message.body.split(' ')[0].strip(config.commandCharacter)
            if potentialCommand in self.commands:
                self.commands[potentialCommand](message) # Invoke the command 

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
        if len(objects) == 0:
            return None
        elif len(objects) > 1:
            log("W: Connection.getRoomByID(): more than 1 Room object for room " + id)
        return objects[0]

    def getRoomByName(self, name):
        '''Gets the Room object for the room of the given name'''
        return self.getRoomByID(toID(name))
    
    def sayIn(self, room, message):
        '''Sends the given message to the given room. Both arguments are strings.'''
        self.websocket.send(room + "|" + message)

    def whisper(self, userid, message):
        '''PMs the given message to the given userid'''
        self.websocket.send("|/pm {user}, {message}".format(user = userid, message = message))
    

if __name__ == "__main__":
    connection = Connection()
    log("I: core.py: opening websocket...")
    connection.websocket.run_forever()
