#!/usr/bin/python3
"""core.py
    core functionality of Expecto Botronum
    by Annika"""

import re
import json
import importlib
import time
import pathlib
import sys
import websocket
import requests


import config
import data
import chatlog

## add modules dir to the path
basePath = pathlib.Path('.')
modulesPath = basePath.joinpath('modules').absolute().resolve()
if str(modulesPath) not in sys.path: sys.path.append(str(modulesPath))

######################
## Helper Functions ##
######################

def log(message):
    """Logs a message to the console according to `config.loglevel`

    Arguments:
        message {string} -- the message to be logged, beginning with E:, W:, I:, or DEBUG:
    """
    # Errors are always logged and warnings if logged go to stderr
    if message[:2] == 'E:' or message[:2] == 'W:' and config.loglevel >= 1: return sys.stderr.write(f"{message}\n")
    if message[:2] == 'I:' and config.loglevel >= 2: return print(message)
    if config.loglevel >= 3: return print(message)

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
    """Represents a room on Pokemon Showdown
    """
    def __init__(self, name, connection):
        """Creates a new Room object

        Arguments:
            name {string} -- the name of the room that the Room object represents (can include spaces/caps)
            connection {Connection} -- the Connection object to use to connect to the room
        """
        self.id = toID(name)
        self.auth = {}
        jpData = data.get("joinphrases")
        self.joinphrases = jpData[self.id] if jpData and self.id in jpData.keys() else {}
        self.connection = connection
        self.join()

    def updateAuth(self, authDict):
        """Updates the auth list for the room based on the given auth dictionary

        Arguments:
            authDict {dictionary} -- dictionary of the changes to the auth list
        """
        for key in authDict.keys():
            if key in self.auth:
                for user in authDict[key]:
                    if user not in self.auth[key]: self.auth[key].add(user)
            else:
                self.auth[key] = set(authDict[key])

    def say(self, message):
        """Sends a message to the room

        Arguments:
            message {string} -- the message to send
        """
        self.connection.send(f"{self.id}|{message}")

    def leave(self):
        """Leaves the room
        """
        log("W: Room.leave() isn't implemented yet")

    def join(self):
        """Joins the room
        """
        self.connection.send(f'|/j {self.id}')
        self.say(f'/cmd roominfo {self.id}')

    def usersWithRankGEQ(self, rank):
        """Gets a set of userids of the roomauth whose room rank is greater than or equal to a certain rank

        Arguments:
            rank {string} -- the minimum rank

        Returns:
            set --  a set of userids for the roomauth whose room rank is greater than or equal to the given rank
        """
        userIDList = set()
        for roomRank in config.roomRanksInOrder[config.roomRanksInOrder.index(rank):]:
            if roomRank in self.auth:
                userIDList = userIDList.union(self.auth[roomRank])
        return userIDList

    def addJoinphrase(self, joinphrase, userid):
        """Adds a joinphrase for the given user ID in the room

        Arguments:
            joinphrase {string} -- the joinphrase
            userid {string that is an ID} -- the ID of the user to give the joinphrase to
        """
        self.joinphrases[userid] = joinphrase
        jpData = data.get("joinphrases") # there might be a race condition here; I'm not sure
        if not jpData: jpData = {}
        jpData[self.id] = self.joinphrases
        data.store("joinphrases", jpData)

    def removeJoinphrase(self, userid):
        """Removes the joinphrase for the given user ID in the room

        Arguments:
            userid {string that is an ID} -- the ID of the user whose joinphrase is being deleted
        """
        if userid in self.joinphrases.keys(): del self.joinphrases[userid]
        jpData = data.get("joinphrases") # there might be a race condition here; I'm not sure
        if not jpData: jpData = {}
        jpData[self.id] = self.joinphrases
        data.store("joinphrases", jpData)

    def __str__(self):
        """String representation of the Room

        Returns:
            string -- representation
        """
        return f"Room: {self.id}; auth: {self.auth}"

################
## User Class ##
################

class User():
    """Represents a user on Pokemon Showdown
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
            action {string} -- the action
                (one of `broadcast`, `addfact`, `hostgame`, `searchlog`, `wall`, `html`, `manage`, or `admin`)
            room {Room} -- the room where the action is taking

        Returns:
            [bool] -- True if the user can do the action and False otherwise
        """
        if not room: return False
        if action not in ['broadcast', 'addfact', 'hostgame', 'searchlog', 'wall', 'html', 'manage', 'admin']:
            log(f"E: User.can(): {action} isn't a valid action")
        return ((action == 'broadcast' and self.id in room.usersWithRankGEQ(config.broadcastRank)) or
            (action == 'addfact' and self.id in room.usersWithRankGEQ(config.addfactRank)) or
            (action == 'hostgame' and self.id in room.usersWithRankGEQ(config.hostgameRank)) or
            (action == 'searchlog' and self.id in room.usersWithRankGEQ(config.searchlogRank)) or
            (action == 'wall' and self.id in room.usersWithRankGEQ('%')) or
            (action == 'html' and self.id in room.usersWithRankGEQ('*')) or
            (action == 'manage' and self.id in room.usersWithRankGEQ(config.manageRank)) or
            self.isAdmin)

    #                       (reason: acronym)
    def PM(self, message): # pylint: disable=invalid-name
        """PMs the user the given message

        Arguments:
            message {string} -- the message to PM the user
        """
        self.connection.whisper(self.id, message)

    def __str__(self):
        """String representation of the User

        Returns:
            string -- representation
        """
        return f"User: {self.name}; id: {self.id}{'; is a bot admin' if self.isAdmin else ''}"

###################
## Message Class ##
###################

class Message():
    """Represents a message sent on Pokemon Showdown
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
        self.senderName = None
        self.connection = connection

        split = raw.split("|")
        self.type = split[1]

        ### Note: there's a lot of reused / copy+paste logic here
        ### It might be worth looking into a better way to format this
        ### tbh all of Message() is kludgy
        if self.type == 'challstr': self.challstr = "|".join(split[2:])
        elif self.type in ['c:', 'c', 'chat']: self.__handleChat(split)
        elif self.type in ['J', 'j', 'join']: self.__handleJoinLeave(split, isJoin = True)
        elif self.type in ['L', 'l', 'leave']: self.__handleJoinLeave(split, isJoin = False)
        elif self.type == 'pm': self.__handlePM(split)
        elif self.type == 'queryresponse': self.__handleQuery(split)
        elif self.type == 'init': pass
        else: log(f"DEBUG: Message() of unknown type {self.type}: {raw}")

        if self.body:
            spaceSplit = self.body.split(' ', 1)
            self.arguments = [spaceSplit[0]]
            if len(spaceSplit) > 1: self.arguments += spaceSplit[1].split(config.separator)

    def respond(self, response):
        """Responds to the message, in a room or in PMs

        If the user cannot broadcast and the command wasn't in PMs or it's not a message that can be responded to, does nothing

        Arguments:
            response {string} -- the response to be sent
        """
        log(f"DEBUG: responding {response}")
        if self.room and self.sender.can("broadcast", self.room):
            self.room.say(response)
        elif self.sender and not self.room:
            self.sender.PM(response)

    def respondHTML(self, html):
        """Responds to the message with a HTML box, in a room or in PMs

        If the user cannot broadcast and the command wasn't in PMs or it's not a message that can be responded to, does nothing

        Arguments:
            html {string} -- the html to be sent
        """
        if self.room and self.sender.can("broadcast", self.room): return self.room.say(f"/adduhtml expectobotronum,{html}")
        if self.sender and not self.room:
            possibleRoomIDs = [r for r in self.connection.getUserRooms(self.sender) \
                if r in self.connection.getUserRooms(self.connection.bot)]
            for possibleRoom in possibleRoomIDs:
                possibleRoom = self.connection.getRoomByID(possibleRoom)
                if possibleRoom and self.connection.bot.can("html", possibleRoom):
                    return possibleRoom.say(f"/pminfobox {self.sender.id}," + html.replace('\n', ''))

    def __handleChat(self, split):
        hasTimestamp = (self.type == 'c:')
        self.type = 'chat'
        self.__setRoom(split)

        currentSlice = 2
        if hasTimestamp:
            self.time = split[currentSlice]
            currentSlice += 1

        username = split[currentSlice].strip()
        currentSlice += 1
        if username[0] in config.roomRanksInOrder:
            rank = username[0]
            username = toID("".join(username[1:]))
            self.room.updateAuth({rank: [username]})

        self.__setSender([None, None, username])
        self.body = "|".join(split[currentSlice:]).strip('\n')

    def __handleJoinLeave(self, split, isJoin = False):
        self.type = 'join' if isJoin else 'leave'
        self.__setRoom(split)
        self.__setSender(split)
        if isJoin: return self.connection.userJoinedRoom(self.sender, self.room)
        return self.connection.userLeftRoom(self.sender, self.room)

    def __handlePM(self, split):
            self.body = "|".join(split[4:]).strip('\n')

    def __handleQuery(self, split):
        query = split[2]
        if query == 'roominfo':
            roomData = json.loads(split[3])
            room = self.connection.getRoomByID(roomData['id']) if 'id' in roomData.keys() else None
            if room and 'auth' in roomData.keys(): room.updateAuth(roomData['auth'])
            if room and 'users' in roomData.keys():
                for user in roomData['users']:
                    userObject = self.connection.getUser(toID(user))
                    if not userObject: userObject = User(toID(user), self.connection)
                    self.connection.userJoinedRoom(userObject, room)

    def __setSender(self, split):
            self.senderName = split[2]
            self.sender = self.connection.getUser(toID(split[2]))
            if not self.sender: self.sender = User(split[2], self.connection)

    def __setRoom(self, split):
            roomid = split[0].strip('>').strip('\n')
            self.room = connection.getRoomByID(roomid if roomid else 'lobby')

    def __str__(self):
        """String representation of the Message

        Returns:
            string -- representation
        """
        buf = "Message"
        if self.body: buf += f" with content {self.body}"
        if self.sender: buf += f" from User({str(self.sender)})"
        if self.senderName: buf += f"sent by {self.senderName}"
        if self.room: buf += f" in Room({str(self.room)})"
        if self.time: buf += f" at {str(self.time)}"
        if self.type: buf += f" of type {self.type}"
        if self.challstr: buf += f" with challstr {self.challstr}"
        if self.arguments: buf += f" with arguments {self.arguments}"
        return buf


######################
## Connection Class ##
######################

class Connection():
    """Represents a connection to Pokemon Showdown
    """
    def __init__(self):
        """Creates a new Connection object
        """
        websocket.enableTrace(False)
        self.websocket = websocket.WebSocketApp(config.websocketURL,
            on_message=self.onMessage,
            on_error=self.onError,
            on_close=self.onClose, on_open=self.onOpen)
        self.roomList = set()
        self.userList = {}
        self.commands = {}
        self.modules = set()
        self.lastSentTime = 0
        self.bot = User(config.username, self)
        self.chatlogger = chatlog.Chatlogger('logs/')
        for module in config.modules:
            # Note: if multiple modules have the same command then the later module will overwrite the earlier.
            try:
                self.commands.update(importlib.import_module(module).Module().commands)
                self.modules.add(module)
            except Exception as err:
                log(f"E: Connection(): error loading module {module}: {str(err)}")
        log(f"I: Connection(): Loaded the following commands: {', '.join(self.commands.keys())}")

    def onError(self, error):
        """Handles errors on the websocket

        Arguments:
            ws {websocket} -- the websocket that's connected to PS
            error {string? probably} -- the error
        """
        log(f"E: Connection.onError(): websocket error: {error}")

    def onClose(self):
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
        if config.logchat: self.chatlogger.handleMessage(message)
        if message.challstr:
            self.login(message.challstr)
        elif message.type == 'join' and message.sender.id in message.room.joinphrases.keys():
            # Handle joinphrases
            message.room.say(message.room.joinphrases[message.sender.id])
        elif message.type in ['chat', 'pm'] and message.body[0] == config.commandCharacter:
            potentialCommand = message.body.split(' ')[0].strip(config.commandCharacter).lower()
            if potentialCommand in self.commands:
                self.commands[potentialCommand](message) # Invoke the command

    def login(self, challstr):
        """Logs into Pokemon Showdown

        Arguments:
            challstr {string} -- the challstr to use to log in
        """
        log("I: Connection.login(): logging in...")
        loginInfo = {'act': 'login', 'name': config.username, 'pass': config.password, 'challstr': challstr}
        loginResponse = requests.post('http://play.pokemonshowdown.com/action.php', data=loginInfo).content
        assertion = json.loads(loginResponse[1:].decode('utf-8'))['assertion']
        self.send(f"|/trn {config.username},0,{assertion}")
        log("I: Connection.login(): joining rooms...")
        for room in config.rooms:
            self.roomList.add(Room(room, self))
        log("I: Connection.login(): rooms joined successfully")

    def send(self, message):
        """Sends a message

        Arguments:
            message {string} -- the message to send
        """
        timeDiff = ((time.time() * 1000.0) - self.lastSentTime) - 600.0 # throttle = 600
        if timeDiff < 0:
            time.sleep((-1 * timeDiff) / 1000.0)
        self.websocket.send(message)
        self.lastSentTime = time.time() * 1000.0

    def getRoomByID(self, roomid):
        """Gets the Room object corresponding to an ID

        Arguments:
            id {string in ID format} -- the room ID (in ID format from toID())

        Returns:
            Room -- a Room object with the given ID
        """
        objects = [room for room in self.roomList if room.id == roomid]
        if len(objects) == 0: return None
        if len(objects) > 1:
            log(f"W: Connection.getRoomByID(): more than 1 Room object for room {roomid}")
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
        self.websocket.send(f"{room}|{message}")

    def whisper(self, userid, message):
        """PMs a message to a user

        Arguments:
            userid {string in ID format} -- the user to PM
            message {string} -- the message to PM
        """
        self.websocket.send(f"|/pm {userid}, {message}")

    def getUserRooms(self, user):
        """Gets a set of the IDs (not objects) of the rooms that the user is in.

        Arguments:
            user {User} -- the user

        Returns:
            set -- the roomids for the user's rooms, or None if the user isn't found
        """
        for possibleUser in self.userList:
            if possibleUser and possibleUser.id == user.id:
                return self.userList[possibleUser]
        return None

    def userJoinedRoom(self, user, room):
        """Handles a user joining a room

        Arguments:
            user {User} -- the user who joined
            room {Room} -- the room they joined
        """
        if not isinstance(self.getUserRooms(user), set):
            self.userList[user] = {room.id}
            return
        for i in self.userList:
            if i.id == user.id:
                self.userList[i].add(room.id)
                return

    def userLeftRoom(self, user, room):
        """Handles a user leaving a room

        Arguments:
            user {User} -- the user who joined
            room {Room} -- the room they joined
        """
        userRooms = self.getUserRooms(user)
        if not isinstance(userRooms, set) or room.id not in userRooms:
            # Do nothing if there's no room set for the user or the user wasn't marked as being in the room
            return
        userRooms.remove(room.id)
        self.userList[self.getUser(user.id)] = userRooms

    def getUser(self, userid):
        """Gets the User object for a given ID

        Arguments:
            userid {string that is an ID} -- the ID of the user to search for

        Returns:
            User || None -- the user, or None if the user isn't in the records
        """
        if userid == self.bot.id: return self.bot
        for user in self.userList:
            if user and user.id == userid:
                return user
        return None

    def __str__(self):
        """String representation of the Connection

        Returns:
            string -- representation
        """
        return f"Connection to {self.websocket.url} with commands {', '.join(self.commands.keys())} \
            in these rooms: {', '.join([str(room.id) for room in self.roomList])}"

if __name__ == "__main__":
    conn = Connection()
    log("I: core.py: opening websocket...")
    conn.websocket.run_forever()
