"""base.py
    contains the base module
    by Annika"""

import re
import threading
from typing import List, Dict

import config
import core
import data


def isAudioURL(url: str) -> bool:
    """Checks if a given URL points to an audio file

    Args:
        url (str): the URL to check

    Returns:
        bool: whether we think it's an audio URL
    """
    if not re.match(r'^https?:\/\/(.*?)\.[a-z]{2,}\/', url):
        # not a URL (probably)
        return False

    return '.vocaroo.com/mp3/' in url or bool(re.match(r'.*\.(mp[34]|wav|ogg)$', url))

def sanitize(text: str) -> str:
    """Sanitizes text, removing command characters

    Args:
        text (str): the raw text

    Returns:
        str: the sanitized text
    """
    return re.sub(r'^([/!\-\.%~])', '\0\0', text)

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self) -> None:
        self.commands = {
            "ping": self.ping, "owo": self.owo, "uwu": self.uwu, "timer": self.timer,
            "help": self.help, "commands": self.help, "guide": self.help,
            "repeat": self.repeat, "addrepeat": self.repeat, "rmrpt": self.removeRepeat, "removerepeat": self.removeRepeat,
            "listrepeats": self.listRepeats, "repeatlist": self.listRepeats,
            "audio": self.audio, "music": self.audio,
        }

    def ping(self, message: core.BotMessage) -> None:
        """Ping: replies "Pong!"

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        message.respond("Pong!")

    def owo(self, message: core.BotMessage) -> None:
        """owo: replaces vowels with owo faces

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        text = config.separator.join(message.arguments[1:])
        for vowel in list("AaEeIiOoUuYy"):
            text = text.replace(vowel, f"{vowel}w{vowel}")
        message.respond(sanitize(text))


    def uwu(self, message: core.BotMessage) -> None:
        """uwu: turns English into weird anime language

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        text = config.separator.join(message.arguments[1:])
        uwuRules = {'r': 'w', 'l': 'w', 'R': 'W', 'L': 'W'}
        for (letter, replacement) in uwuRules.items():
            text = text.replace(letter, replacement)
        message.respond(sanitize(text))

    def timer(self, message: core.BotMessage) -> None:
        """timer: evaluates the given Python expression

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if len(message.arguments) not in range(1, 4):
            message.respond(f"Usage: ``{config.commandCharacter}timer <duration>, <optional message>``")
            return
        response = "/wall " if message.type == 'pm' or message.connection.this.can('wall', message.room) else ""
        response += message.arguments[2] if len(message.arguments) > 2 else f"Timer set by {message.sender.name} is up"

        try:
            duration = float(message.arguments[1])
        except ValueError:
            message.respond(f"{message.arguments[1]} isn't a valid duration")
            return
        t = threading.Timer(duration, message.respond, args=[response])
        t.daemon = True
        t.start()

    def repeat(self, message: core.BotMessage) -> None:
        """repeat: repeats a message

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if len(message.arguments) < 3:
            return message.respond(f"Usage: ``{config.commandCharacter}repeat <message>, <interval in minutes>``.")
        if not message.room: return message.respond("Use this command in a room.")

        if not message.sender.can('searchlog', message.room): return message.respond("Permission denied.")

        msg = config.separator.join(message.arguments[1:-1])
        try:
            times = int(message.arguments[-1])
        except ValueError:
            times = -1
        if times < 1: return message.respond("You must specify an interval of at least 1 minute.")

        for repeat in data.get("repeats") or {}:
            if msg in repeat: return message.respond("That message is already being repeated.")

        repeats: Dict[str, List[Dict[str, int]]] = data.get("repeats") or {}
        if message.room.id not in repeats: repeats[message.room.id] = []
        repeats[message.room.id].append({msg: times})
        data.store("repeats", repeats)

        message.room.runRepeat({msg: times})
        return message.respond("Added the repeating message!")

    def removeRepeat(self, message: core.BotMessage) -> None:
        """removerepeat: removes a repeat

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if len(message.arguments) < 2:
            return message.respond(f"Usage: ``{config.commandCharacter}removerepeat <message>``.")

        if not message.sender.can('searchlog', message.room): return message.respond("Permission denied.")

        msg = config.separator.join(message.arguments[1:])
        repeats = data.get("repeats")
        if not repeats or message.room.id not in repeats:
            return message.respond(f"There are no repeats for the room '{message.room.id}'.")

        repeatFound = False
        newRepeats = []
        for repeat in repeats[message.room.id]:
            if msg in repeat:
                repeatFound = True
                continue
            newRepeats.append(repeat)
        if not repeatFound: return message.respond("No repeat found.")

        repeats[message.room.id] = newRepeats
        data.store("repeats", repeats)
        return message.respond("Repeat removed!")

    def listRepeats(self, message: core.BotMessage) -> None:
        """listrepeats: lists repeats

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        room = message.room
        if not room:
            if len(message.arguments) != 2:
                return message.respond("You must specify a room when using this command in PMs.")
            room = message.connection.getRoom(message.arguments[1])
            if not room:
                return message.respond(f"I'm not in the room '{message.arguments[1]}'.")

        if not message.sender.can('searchlog', room): return message.respond("Permission denied.")
        repeats = data.get("repeats")
        if not (repeats and room.id in repeats and repeats[room.id]):
            return message.respond(f"There are no repeats for the room '{room.id}'")
        htmlBuf = f"<details><summary>Repeats for the room <strong>{room.id}</strong></summary><ul>"
        for repeat in repeats[room.id]:
            htmlBuf += f"<li>Repeated every {list(repeat.values())[0]} minutes: \"{list(repeat.keys())[0]}\"</li>"
        htmlBuf += "</ul></details>"
        print(htmlBuf)
        return message.respondHTMLPatched(htmlBuf)

    def audio(self, message: core.BotMessage) -> None:
        """audio: displays audio in the room

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if len(message.arguments) < 2:
            return message.respond(f"Usage: ``{ config.commandCharacter}audio <URL to audio file>``.")

        url = ','.join(message.arguments[1:]).strip()
        if not isAudioURL(url):
            return message.respond(
                "You must specify a valid URL beginning with ``http://`` or ``https://``; the URL must refer to an audio file."
            )

        return message.respondHTMLPatched(f'<audio controls src="{url}"></audio>')

    def help(self, message: core.BotMessage) -> None:
        """Help

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        return message.respond(
            "Expecto Botronum guide: https://github.com/AnnikaCodes/expecto-botronum/blob/master/README.md#commands"
        )

    def __str__(self) -> str:
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Base module: provides basic bot functionality. Commands: {', '.join(self.commands.keys())}"
