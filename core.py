#!/usr/bin/env python3
"""core.py
    core functionality of Expecto Botronum
    by Annika"""

import re
import pathlib
import sys
import time
import importlib
import threading
from typing import Dict, Tuple, List, Any

import psclient # type: ignore

import config
import rust_chatlogger # type: ignore
import data
from translations import translate

JOINPHRASE_COOLDOWN = 60 * 60 * 60 # 60 minutes

BOLD_REGEX = re.compile(r'(.*)(?!``)(\*\*)([^\s])(.*)(\*\*)(?!``)(.*)')
CAPS_REGEX = re.compile(r'(.*)([A-Z]{7,})|([A-Z]{3,}(.{0,3})[A-Z]{3,})(.*)')

VERBALWARN_THRESHOLD = 1
WARN_THRESHOLD = 2
MUTE_THRESHOLD = 3
HOURMUTE_THRESHOLD = 4

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
        self.lastJoinphraseTimes: Dict[str, float] = {}

        repeats = data.get("repeats")
        if repeats and self.id in repeats and repeats[self.id]:
            for repeat in repeats[self.id]:
                self.runRepeat(repeat)

        moderation = data.get("moderation")
        if moderation and self.id in moderation:
            self.moderation = moderation.get(self.id)
        else:
            self.moderation = None

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

    def runJoinphrase(self, userid: str) -> bool:
        """Handles joinphrases for a particular user

        Args:
            userid (str): the user's ID

        Returns:
            bool: True if a joinphrase was sent and False otherwise
        """
        if userid not in self.joinphrases.keys(): return False
        if userid in self.lastJoinphraseTimes and self.lastJoinphraseTimes[userid] > time.time() - JOINPHRASE_COOLDOWN:
            return False
        self.say(f"(__{userid}__) {self.joinphrases[userid]}")
        self.lastJoinphraseTimes[userid] = time.time()
        return True

    def runRepeat(self, repeat: Dict[str, int]) -> None:
        """Runs a repeat in the room

        Args:
            repeat (Dict[str, int]): [description]
        """
        def runner(msg: str, interval: int) -> None:
            repeats = data.get('repeats')
            if not repeats or self.id not in repeats or msg not in [list(r.keys())[0] for r in repeats[self.id]]: return
            self.say(msg)
            t = threading.Timer(interval * 60, runner, args=[msg, interval])
            t.daemon = True
            t.start()

        message = list(repeat.keys())[0]
        runner(message, repeat[message])

    def setModerationType(self, moderationType: str, isEnabled: bool) -> None:
        """Enables a type of automated moderation in the room

        Args:
            t (str): the moderation type, e.g. bold
        """
        if not self.moderation: self.moderation = {}
        self.moderation[moderationType] = isEnabled
        moderation = data.get("moderation") or {}
        moderation[self.id] = self.moderation
        data.store("moderation", moderation)

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

    def respondHTML(self, html: str) -> None:
        """Responds with HTML

        Args:
            html (str): the HTML code
        """
        if self.room and self.connection.this.can("html", self.room):
            return self.room.say(f"/addhtmlbox {html}")
        return super().respondHTML(html)

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
            loglevel=config.loglevel
        )
        self.commands: Dict[str, Any] = {}
        self.modules: set = set()
        # We have our own chatlogger that takes its own arguments.
        self.rustChatlogger = rust_chatlogger.Chatlogger("logs.db") if config.logchat else None
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
        self.send('|/avatar 50')
        for room in config.rooms:
            BotRoom(room, self)

    def userJoinedRoom(self, user: psclient.User, room: psclient.Room) -> None:
        return super().userJoinedRoom(BotUser(user.name, self), room)

    def __str__(self) -> str:
        """String representation, now with commands
        """
        return super().__str__() + f"with commands {', '.join(self.commands.keys())}" if self.commands else ""

VALID_AUTOMOD_TYPES = ['bold', 'caps', 'flooding']

class Automod:
    """Handles automatic moderation"""
    def __init__(self) -> None:
        # Dict[roomid, Dict[userid, punishment points]]
        self.points: Dict[str, Dict[str, int]] = {}
        # Dict[roomid, Tuple[userid, lines]]
        self.flooders: Dict[str, Tuple[str, int]] = {}

    def filterMessage(self, message: BotMessage) -> None:
        """Filters incoming messages and moderates on them if necessary

        Args:
            message (BotMessage): the message that is being filtered
        """
        if not message.sender or not message.room or not message.room.moderation: return
        if not self.points.get(message.room.id):
            self.points[message.room.id] = {}

        flooder = self.flooders.get(message.room.id)
        if flooder and len(flooder) >= 2 and message.sender.id == flooder[0]:
            self.flooders[message.room.id] = (message.sender.id, flooder[1] + 1)
        else:
            self.flooders[message.room.id] = (message.sender.id, 0)

        if message.sender.can('broadcast', message.room): return

        # Automatically moderate for bold
        if message.room.moderation.get('bold') and BOLD_REGEX.match(message.body):
            if not self.points[message.room.id].get(message.sender.id):
                self.points[message.room.id][message.sender.id] = 0
            self.points[message.room.id][message.sender.id] += 1
            return self.runPunish(message, translate(message.room, "do not abuse bold formatting"))

        # Automatically moderate for caps
        if message.room.moderation.get('caps') and CAPS_REGEX.match(message.body):
            if not self.points[message.room.id].get(message.sender.id):
                self.points[message.room.id][message.sender.id] = 0
            self.points[message.room.id][message.sender.id] += 1
            return self.runPunish(message, translate(message.room, "do not abuse capital letters"))

        # Automatically moderate for flooding
        if message.room.moderation.get('flooding') and self.flooders[message.room.id][1] > 4:
            if not self.points[message.room.id].get(message.sender.id):
                self.points[message.room.id][message.sender.id] = 0
            self.points[message.room.id][message.sender.id] += 1
            return self.runPunish(message, translate(message.room, "do not flood the chat"))

    def runPunish(self, message: BotMessage, reason: str) -> None:
        """Checks a user's points and moderates as needed

        Args:
            message (BotMessage): the message invoking this
            reason (str): the reason
        """
        if self.points[message.room.id][message.sender.id] >= HOURMUTE_THRESHOLD:
            self.points[message.room.id][message.sender.id] = 1
            self.punish("hourmute", message.room, message.sender.id, reason)
        elif self.points[message.room.id][message.sender.id] >= MUTE_THRESHOLD:
            self.punish("mute", message.room, message.sender.id, reason)
        elif self.points[message.room.id][message.sender.id] >= WARN_THRESHOLD:
            self.punish("warn", message.room, message.sender.id, reason)
        elif self.points[message.room.id][message.sender.id] >= VERBALWARN_THRESHOLD:
            message.room.say(f"{message.sender.name}, {reason}.")

    def punish(self, punishment: str, room: BotRoom, userid: str, reason: str) -> None:
        """Automatically punishes a user

        Args:
            userid (str): the user ID to be muted
            reason (str): the reason for the mute
        """
        room.say(f"/{punishment} {userid}, automated moderation: {reason}")
        if punishment != 'roomban': room.say(f"/hidealtstext {userid}")


def handleMessage(connection: BotConnection, message: psclient.Message) -> None:
    """Handles messages from the websocket
    """
    automod.filterMessage(message)
    if message.type == 'join':
        # Handle joinphrases
        message.room.runJoinphrase(message.sender.id)
    elif message.type in ['chat', 'pm']:
        if connection.rustChatlogger:
            connection.rustChatlogger.handle_message(
                message.type, # `kind` in Rust
                message.room.id if message.room else None, # `room_id` in Rust
                int(message.time) if message.time else None, # `timestamp` in Rust
                message.sender.id, # `sender_id` in Rust
                message.senderName, # `sender_name` in Rust
                message.body, # `body` in Rust
            )
        if message.body[0] == config.commandCharacter:
            potentialCommand: str = message.body.split(' ')[0].strip(config.commandCharacter).lower()
            if potentialCommand in connection.commands:
                connection.commands[potentialCommand](BotMessage(message.raw, connection)) # Invoke the command
    elif message.type == 'pm' and message.sender.id != connection.this.id:
        BotMessage(message.raw, connection).respond(
            "Hi! I'm a computer program written by Annika, not a real person. " +
            "If you need a staff member, PM someone else (with %, @, or # before their name), or " +
            "type ``/helpticket`` to get assistance from global staff. " +
            f"To see my commands, type ``{config.commandCharacter}help``!"
        )

if __name__ == "__main__":
    conn: BotConnection = BotConnection()
    client: psclient.PSClient = psclient.PSClient(conn)
    automod = Automod()
    log("I: core.py: client connecting...")
    client.connect()
