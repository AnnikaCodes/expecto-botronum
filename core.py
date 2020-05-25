#!/usr/bin/python3

import config
import re
import websocket
import requests
import json
import importlib

################## core.py #####################
## core functionality of Expecto Botronum     ##
## by Annika                                  ##
################################################

######################
## Helper Functions ##
######################

def log(message):
    """Logs a message to the console according to `config.loglevel`

    Arguments:
        message {string} -- the message to be logged, beginning with E:, W:, I:, or DEBUG:
    """
    if config.loglevel > 2 or message[:2] == 'E:':
        # Errors are always logged and everything in debug mode is logged.
        print(message)
    elif message[:2] == 'W:' and config.loglevel >= 1:
        print(message)
    elif message[:2] == 'I:' and config.loglevel >= 2:
        print(message)

def toID(string):
    """Converts a string into an ID

    Arguments:
        string {string} -- the string to be converted

    Returns:
        [string] -- the ID
    """
    return re.sub('[^0-9a-zA-Z]+', '', string).lower()

################
## Room Class ##
################

class Room():
    """Represents a room on Pokémon Showdown
    """
    def __init__(self, name, connection):
        """Creates a new Room object

        Arguments:
            name {string} -- the name of the room that the Room object represents (can include spaces/caps)
            connection {Connection} -- the Connection object to use to connect to the room
        """
        self.id = toID(name)
        self.auth = {}
        self.connection = connection
        self.join()

    def updateAuth(self, authDict):
        """Updates the auth list for the room based on the given auth dictionary

        Arguments:
            authDict {dictionary} -- dictionary of the changes to the auth list
        """
        for key in authDict.keys():
            if key in self.auth:
                self.auth[key] += authDict[key]
            else:
                self.auth[key] = authDict[key]

    def say(self, message):
        """Sends a message to the room

        Arguments:
            message {string} -- the message to send
        """
        self.connection.send(self.id + "|" + message)

    def leave(self):
        """Leaves the room
        """
        log("W: Room.leave() isn't implemented yet")

    def join(self):
        """Joins the room
        """
        self.connection.send("|/j " + self.id)
        self.say('/roomauth')

    def usersWithRankGEQ(self, rank):
        """Gets a list of userids of the roomauth whose room rank is greater than or equal to a certain rank

        Arguments:
            rank {string} -- the minimum rank

        Returns:
            [string] --  a list of userids for the roomauth whose room rank is greater than or equal to the given rank
        """
        userIDList = []
        for rank in config.roomRanksInOrder[config.roomRanksInOrder.index(rank):]:
            if rank in self.auth:
                userIDList.extend(self.auth[rank])
        return userIDList

################
## User Class ##
################

class User():
    """Represents a user on Pokémon Showdown
    """
    def __init__(self, name, connection):
        """User()

        Arguments:
            name {string} -- the username
            connection {Connection} -- the connection to access PS with
        """
        self.name = name
        self.id = toID(name)
        self.isAdmin = self.id in config.sysops
        self.connection = connection

    def can(self, action, room):
        """Checks if the user may perform an action

        Arguments:
            action {string} -- the action (one of `broadcast`, `addfact`, `hostgame`, `manage`, or `admin`)
            room {Room} -- the room where the action is taking 

        Returns:
            [bool] -- True if the user can do the action and False otherwise
        """
        if action not in ['broadcast', 'addfact', 'hostgame', 'manage', 'admin']:
            log("E: User.can(): {action} isn't a valid action".format(action=action))
        return ((action == 'broadcast' and self.id in room.usersWithRankGEQ(config.broadcastRank)) or
            (action == 'addfact' and self.id in room.usersWithRankGEQ(config.addfactRank)) or
            (action == 'hostgame' and self.id in room.usersWithRankGEQ(config.hostgameRank)) or
            (action == 'manage' and self.id in room.usersWithRankGEQ(config.manageRank)) or
            self.isAdmin)

    def PM(self, message):
        """PMs the user the given message

        Arguments:
            message {string} -- the message to PM the user
        """
        self.connection.whisper(self.id, message)

###################
## Message Class ##
###################

class Message():
    """Represents a message sent on Pokémon Showdown
    """
    def __init__(self, raw, connection):
        """Creates a new Message object

        Arguments:
            raw {string} -- the raw data of the message
            connection {Connection} -- the connection the message was recieved on
        """
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
    
    def respond(self, response):
        """Responds to the message, in a room or in PMs

        If the user cannot broadcast and the command wasn't in PMs or it's not a message that can be responded to, does nothing

        Arguments:
            response {string} -- the response to be sent
        """ 
        log("DEBUG: responding " + response)       
        if self.room and self.sender.can("broadcast", self.room):
            self.room.say(response)
        elif self.sender and not self.room:
            self.sender.PM(response)

######################
## Connection Class ##
######################

class Connection():
    """Represents a connection to Pokémon Showdown
    """
    def __init__(self):
        """Creates a new Connection object
        """
        websocket.enableTrace(False)
        self.websocket = websocket.WebSocketApp(config.websocketURL,
            on_message = self.onMessage,
            on_error = self.onError,
            on_close = self.onClose, on_open = self.onOpen)
        self.roomList = []
        self.commands = {}
        for module in config.modules:
            self.commands.update(importlib.import_module(module).Module().commands)
            # Note: if multiple modules have the same command then the later module will overwrite the earlier.
        log("I: Connection(): Loaded the following commands: " + ", ".join(self.commands.keys()))

    def onError(self, ws, error):
        """Handles errors on the websocket

        Arguments:
            ws {websocket} -- the websocket that's connected to PS
            error {string? probably} -- the error
        """        
        log("E: Connection.onError(): websocket error: {error}".format(error = error))

    def onClose(self, ws):
        """Logs when the connection closes

        Arguments:
            ws {websocket} -- the websocket that's connected to PS
        """        
        log("I: Connection.onClose(): websocket closed")

    def onOpen(self):
        """Logs when the websocket is opened
        """        
        log("I: Connection.onOpen(): websocket successfully opened")

    def onMessage(self, rawMessage):
        """Handles new messages from the websocket, creating a Message object and invoking commands

        Arguments:
            rawMessage {string} -- the raw message data
        """        
        message = Message(rawMessage, self)
        if message.challstr:
            self.login(message.challstr)
        elif message.type in ['chat', 'pm'] and message.body[0] == config.commandCharacter:
            potentialCommand = message.body.split(' ')[0].strip(config.commandCharacter)
            if potentialCommand in self.commands:
                self.commands[potentialCommand](message) # Invoke the command 

    def login(self, challstr):
        """Logs into Pokémon Showdown

        Arguments:
            challstr {string} -- the challstr to use to log in
        """        
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
        """Sends a message

        Arguments:
            message {string} -- the message to send
        """        
        self.websocket.send(message)

    def getRoomByID(self, id):
        """Gets the Room object corresponding to an ID

        Arguments:
            id {string in ID format} -- the room ID (in ID format from toID())

        Returns:
            Room -- a Room object with the given ID
        """        
        objects = [room for room in self.roomList if room.id == id]
        if len(objects) == 0:
            return None
        elif len(objects) > 1:
            log("W: Connection.getRoomByID(): more than 1 Room object for room " + id)
        return objects[0]

    def getRoomByName(self, name):
        """Gets the Room object with the given name

        Arguments:
            name {string} -- the name of the room

        Returns:
            Room -- a Room object with the given name
        """        
        return self.getRoomByID(toID(name))
    
    def sayIn(self, room, message):
        """Sends a message to a room.

        Arguments:
            room {Room} -- the room to send the message to
            message {string} -- the message to send
        """
        self.websocket.send(room + "|" + message)

    def whisper(self, userid, message):
        """PMs a message to a user

        Arguments:
            userid {string in ID format} -- the user to PM
            message {string} -- the message to PM
        """
        self.websocket.send("|/pm {user}, {message}".format(user = userid, message = message))
    
if __name__ == "__main__":
    connection = Connection()
    log("I: core.py: opening websocket...")
    connection.websocket.run_forever()
