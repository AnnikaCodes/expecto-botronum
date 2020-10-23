"""logsearch.py
    handles searching chat logs
    by Annika"""

import psclient # type: ignore

import config
import core

MAX_MESSAGES = 500
TOPUSERS = 50

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self) -> None:
        self.commands = {
            "logsearch": self.logsearch, "searchlogs": self.logsearch, "sl": self.logsearch,
            "linecount": self.linecount, "topusers": self.topusers
        }

    def logsearch(self, message: core.BotMessage) -> None:
        """Searches logs

        Args:
            message (message: core.BotMessage) -> None: the Message object that invoked the command
        """
        if len(message.arguments) < 2:
            return message.respond(f"Usage: ``{config.commandCharacter}logsearch <room>, [optional user], [optional keyword]``.")
        if not message.connection.rustChatlogger: return message.respond("There is currently no chatlogger loaded.")
        roomID = psclient.toID(message.arguments[1]).lower()
        userID = psclient.toID(message.arguments[2]).lower() if len(message.arguments) > 2 else None
        keywords = message.arguments[3:] if len(message.arguments) > 3 else None

        room = message.connection.getRoom(roomID)
        if not room: return message.respond(f"Invalid room: {roomID}")
        if not message.sender.can("searchlog", room): return message.respond("Permission denied.")

        message.respond(
            f"Fetching the {MAX_MESSAGES} most recent messages in the room {roomID}" +
            (f" sent by the user '{userID}'" if userID else "") +
            (f" containing all of the following keywords: {', '.join(keywords)}" if keywords else "") +
            "."
        )

        return message.respondHTML(message.connection.rustChatlogger.html_search(
            roomID,
            userID or None,
            None, # `oldest` param in Rust
            keywords or None,
            MAX_MESSAGES
        ))

    def linecount(self, message: core.BotMessage) -> None:
        """Gets a user's linecount

        Args:
            message (message: core.BotMessage) -> None: the Message object that invoked the command
        """
        if len(message.arguments) < 3:
            return message.respond(f"Usage: ``{config.commandCharacter}linecount <user>, <room>, [optional number of days]``.")

        userID = psclient.toID(message.arguments[1])
        roomID = psclient.toID(message.arguments[2])
        try:
            days = int(message.arguments[3])
        except (IndexError, ValueError):
            days = 30

        room = message.connection.getRoom(roomID)
        if not message.connection.rustChatlogger: return message.respond("There is currently no chatlogger loaded.")
        if not room: return message.respond(f"Invalid room: {roomID}")
        if not message.sender.can("searchlog", room): return message.respond("Permission denied.")

        message.respondHTML(message.connection.rustChatlogger.linecount_html(roomID, userID, days))

    def topusers(self, message: core.BotMessage) -> None:
        """Gets the top users of a room

        Args:
            message (message: core.BotMessage) -> None: the Message object that invoked the command
        """
        if len(message.arguments) < 2:
            return message.respond(f"Usage: ``{config.commandCharacter}topusers <room>, [optional number of days]``.")

        roomID = psclient.toID(message.arguments[1])
        try:
            days = int(message.arguments[2])
        except (IndexError, ValueError):
            days = 30

        room = message.connection.getRoom(roomID)
        if not message.connection.rustChatlogger: return message.respond("There is currently no chatlogger loaded.")
        if not room: return message.respond(f"Invalid room: {roomID}")
        if not message.sender.can("searchlog", room): return message.respond("Permission denied.")
        message.respond("Please wait; fetching userstats...")

        return message.respondHTML(message.connection.rustChatlogger.topusers_html(
            roomID,
            days,
            30
        ))

    def __str__(self) -> str:
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Logsearch module: handles searching chatlogs. Commands: {', '.join(self.commands.keys())}"
