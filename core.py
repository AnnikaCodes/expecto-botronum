#!/usr/bin/python3
"""core.py
    core functionality of Expecto Botronum
    by Annika"""

import pathlib
import sys
import importlib
from typing import Dict, Any, List

import psclient # type: ignore

import config
import data
## add modules dir to the path
basePath = pathlib.Path('.')
modulesPath = basePath.joinpath('modules').absolute().resolve()
privateModulesPath = modulesPath.joinpath('private').absolute().resolve()
if str(modulesPath) not in sys.path: sys.path.append(str(modulesPath))
if str(privateModulesPath) not in sys.path: sys.path.append(str(privateModulesPath))

def log(string: str) -> None:
    """Bootstrapped off of psclient.log(), but using our own loglevel

    Args:
        string (str): the string to log
    """
    psclient.LOGLEVEL = config.loglevel
    return psclient.log(string)

class BotUser(psclient.User):
    """The original psclient.User class extended for the bot
    """
    def can(self, action: str, room: psclient.Room) -> bool:
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
            self.id in config.sysops
        )

class BotRoom(psclient.Room):
    """The original psclient.Room class from the ps-client package, extended for the bot to include joinphrase storage
    """
    def __init__(self, name: str, connection: psclient.PSConnection):
        super().__init__(name, connection)
        jpData = data.get("joinphrases")
        self.joinphrases = jpData[self.id] if jpData and self.id in jpData.keys() else {}

    def addJoinphrase(self, joinphrase: str, userid: str) -> None:
        """Adds a joinphrase for the given user ID in the room
        Arguments:
            joinphrase {string} -- the joinphrase
            userid {string that is an ID} -- the ID of the user to give the joinphrase to
        """
        self.joinphrases[userid] = joinphrase
        jpData: dict = data.get("joinphrases") or {} # there might be a race condition here; I'm not sure
        jpData[self.id] = self.joinphrases
        data.store("joinphrases", jpData)

    def removeJoinphrase(self, userid: str) -> None:
        """Removes the joinphrase for the given user ID in the room
        Arguments:
            userid {string that is an ID} -- the ID of the user whose joinphrase is being deleted
        """
        if userid in self.joinphrases.keys(): del self.joinphrases[userid]
        jpData: dict = data.get("joinphrases") or {} # there might be a race condition here; I'm not sure
        jpData[self.id] = self.joinphrases
        data.store("joinphrases", jpData)

class BotMessage(psclient.Message):
    """The original psclient.Message class from the ps-client package, extended for the bot to include an arguments attribute
    """
    def __init__(self, raw: str, connection: psclient.PSConnection):
        super().__init__(raw, connection)
        # Expecto Botronum uses an arguments attribute to make commands easier, which is too specific for the ps-client package.
        if self.body:
            spaceSplit: list = self.body.split(' ', 1)
            self.arguments: List[str] = [spaceSplit[0]]
            if len(spaceSplit) > 1: self.arguments += spaceSplit[1].split(config.separator)

    def respond(self, response: str) -> None:
        """Responds to the message, in a room or in PMs
        If the user cannot broadcast and the command wasn't in PMs or it's not a message that can be responded to, does nothing
        Arguments:
            response {string} -- the response to be sent
        """
        if self.room and self.sender.can("broadcast", self.room):
            self.room.say(response)
        elif self.sender and not self.room:
            self.sender.PM(response)

    def __str__(self) -> str:
        return super().__str__() + f" with arguments {self.arguments}" if self.arguments else ""

class BotConnection(psclient.PSConnection):
    """The original psclient.PSConnection class from the ps-client package, extended with bot-specific features
    """
    def __init__(self) -> None:
        super().__init__(
            config.username,
            config.password,
            onParsedMessage=handleMessage,
            url=config.websocketURL,
            chatlogger=psclient.chatlog.Chatlogger("logs/") if config.logchat else None,
            loglevel=config.loglevel
        )
        self.commands: Dict[str, Any] = {}
        self.modules: set = set()
        self.this: BotUser = BotUser(self.this.name, self)
        for module in config.modules:
            # Note: if multiple modules have the same command then the later module will overwrite the earlier.
            try:
                self.commands.update(importlib.import_module(module).Module().commands) # type: ignore
                self.modules.add(module)
            except Exception as err:
                log(f"E: core.BotConnection(): error loading module {module}: {str(err)}")
        log(f"I: core.BotConnection(): Loaded the following commands: {', '.join(self.commands.keys())}")

    def login(self, challstr: str) -> None:
        """Logs in to Pokemon Showdown
        """
        super().login(challstr)
        for room in config.rooms:
            BotRoom(room, self)

    def userJoinedRoom(self, user: psclient.User, room: psclient.Room) -> None:
        return super().userJoinedRoom(BotUser(user.name, self), room)

    def __str__(self) -> str:
        """String representation, now with commands
        """
        return super().__str__() + f"with commands {', '.join(self.commands.keys())}" if self.commands else ""

def handleMessage(connection: BotConnection, message: psclient.Message) -> None:
    """Handles messages from the websocket
    """
    if message.type == 'join' and message.sender.id in message.room.joinphrases.keys():
        # Handle joinphrases
        message.room.say(message.room.joinphrases[message.sender.id])
    elif message.type in ['chat', 'pm'] and message.body[0] == config.commandCharacter:
        potentialCommand: str = message.body.split(' ')[0].strip(config.commandCharacter).lower()
        if potentialCommand in connection.commands:
            connection.commands[potentialCommand](BotMessage(message.raw, connection)) # Invoke the command

if __name__ == "__main__":
    conn: BotConnection = BotConnection()
    client: psclient.PSClient = psclient.PSClient(conn)
    log("I: core.py: client connecting...")
    client.connect()
