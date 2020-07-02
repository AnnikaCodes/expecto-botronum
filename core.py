#!/usr/bin/python3
"""core.py
    core functionality of Expecto Botronum
    by Annika"""

import pathlib
import sys
import importlib
import psclient

import config
import data

## add modules dir to the path
basePath = pathlib.Path('.')
modulesPath = basePath.joinpath('modules').absolute().resolve()
if str(modulesPath) not in sys.path: sys.path.append(str(modulesPath))

def log(string):
    """Bootstrapped off of psclient.log(), but using our own loglevel

    Args:
        string (string): the string to log
    """
    psclient.LOGLEVEL = config.loglevel
    return psclient.log(string)

class User(psclient.User):
    """The original psclient.User class extended for the bot
    """
    def can(self, action, room):
        """Checks if the user may perform an action -- overloads the ps-client package with custom permissions checking
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
        return (
            (action == 'broadcast' and self.id in room.usersWithRankGEQ(config.broadcastRank)) or
            (action == 'addfact' and self.id in room.usersWithRankGEQ(config.addfactRank)) or
            (action == 'hostgame' and self.id in room.usersWithRankGEQ(config.hostgameRank)) or
            (action == 'searchlog' and self.id in room.usersWithRankGEQ(config.searchlogRank)) or
            (action == 'wall' and self.id in room.usersWithRankGEQ('%')) or
            (action == 'html' and self.id in room.usersWithRankGEQ('*')) or
            (action == 'manage' and self.id in room.usersWithRankGEQ(config.manageRank)) or
            (action == 'admin' and self.id in config.sysops)
        )

class Room(psclient.Room):
    """The original psclient.Room class from the ps-client package, extended for the bot to include joinphrase storage
    """
    def __init__(self, name, connection):
        super().__init__(name, connection)
        jpData = data.get("joinphrases")
        self.joinphrases = jpData[self.id] if jpData and self.id in jpData.keys() else {}

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

class Message(psclient.Message):
    """The original psclient.Message class from the ps-client package, extended for the bot to include an arguments attribute
    """
    def __init__(self, raw, connection):
        super().__init__(raw, connection)
        # Expecto Botronum uses an arguments attribute to make commands easier, which is too specific for the ps-client package.
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
        if self.room and self.sender.can("broadcast", self.room):
            self.room.say(response)
        elif self.sender and not self.room:
            self.sender.PM(response)

    def _setSender(self, split):
        """Sets the .sender attribute based on split[2]. Overloads psclient.User._setSender()
        Args:
            split (list): the split raw message
        """
        self.senderName = split[2]
        self.sender = self.connection.getUser(psclient.toID(split[2]))
        if not self.sender: self.sender = User(split[2], self.connection)

    def __str__(self):
        return super().__str__() + f" with arguments {self.arguments}" if self.arguments else ""

class Connection(psclient.PSConnection):
    """The original psclient.PSConnection class from the ps-client package, extended with bot-specific features
    """
    def __init__(self):
        super().__init__(
            config.username,
            config.password,
            onParsedMessage=handleMessage,
            url=config.websocketURL,
            chatlogger=psclient.chatlog.Chatlogger("logs/") if config.logchat else None,
            loglevel=config.loglevel
        )
        self.commands = {}
        self.modules = set()
        self.this = User(self.this.name, self)
        for module in config.modules:
            # Note: if multiple modules have the same command then the later module will overwrite the earlier.
            try:
                self.commands.update(importlib.import_module(module).Module().commands)
                self.modules.add(module)
            except Exception as err:
                log(f"E: core.Connection(): error loading module {module}: {str(err)}")
        log(f"I: core.Connection(): Loaded the following commands: {', '.join(self.commands.keys())}")

    def userJoinedRoom(self, user, room):
        return super().userJoinedRoom(User(user.name, self), room)

    def __str__(self):
        """String representation, now with commands
        """
        return super().__str__() + f"with commands {', '.join(self.commands.keys())}" if self.commands else ""

def handleMessage(connection, message):
    """Handles messages from the websocket
    """
    if message.type == 'join' and message.sender.id in message.room.joinphrases.keys():
        # Handle joinphrases
        message.room.say(message.room.joinphrases[message.sender.id])
    elif message.type in ['chat', 'pm'] and message.body[0] == config.commandCharacter:
        potentialCommand = message.body.split(' ')[0].strip(config.commandCharacter).lower()
        if potentialCommand in connection.commands:
            connection.commands[potentialCommand](message) # Invoke the command

if __name__ == "__main__":
    conn = Connection()
    client = psclient.PSClient(conn)
    log("I: core.py: client connecting...")
    client.connect()
