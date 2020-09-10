"""automod.py
    provides automatic moderation features for rooms
    by Annika"""

from typing import Dict, Any
import psclient # type: ignore
import core

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self) -> None:
        self.commands: Dict[str, Any] = {
            "enablemoderation": self.changeModeration, "disablemoderation": self.changeModeration,
            "moderation": self.viewModerationSettings, "viewmoderation": self.viewModerationSettings
        }

    def changeModeration(self, message: core.BotMessage) -> None:
        """Changes moderation settings

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        def usage() -> None:
            return message.respond(f"Usage: ``{message.arguments[0]} [optional room], <moderation type>``.")
        if len(message.arguments) < 2: return usage()

        isEnabling = 'enable' in message.arguments[0]

        room = message.connection.getRoom(message.arguments[1])

        index = 2
        if not room:
            if not message.room:
                return message.respond("You must specify a room in PMs.")
            room = message.room
            index = 1

        if len(message.arguments) < index + 1: return usage()

        if not message.sender.can("manage", room):
            return message.respond("Permission denied.")

        moderationType = psclient.toID(message.arguments[index])
        if moderationType not in core.VALID_AUTOMOD_TYPES:
            return message.respond(
                f"'{moderationType}' is not a valid moderation type. Use one of: {', '.join(core.VALID_AUTOMOD_TYPES)}"
            )

        room.setModerationType(moderationType, isEnabling)
        return message.respond(
            f"Successfully {'enabled' if isEnabling else 'disabled'} moderation for {moderationType} in {room.id}!"
        )

    def viewModerationSettings(self, message: core.BotMessage) -> None:
        """Displays information about a room's moderation settings

        Args:
            message (core.BotMessage): the Message object that invoked the command
        """
        room = message.room
        if not room and len(message.arguments) > 1:
            room = message.connection.getRoom(message.arguments[1])
        if not room:
            return message.respond("You must specify a valid room when using this command in PMs.")

        if not message.sender.can("searchlog", room): return message.respond("Permission denied.")

        moderation = room.moderation or {}
        buf = f"Moderation settings for room **``{room.id}``**: "
        buf += ', '.join(
            [f"**{thing}**: {'enabled' if moderation.get(thing) else 'disabled'}" for thing in core.VALID_AUTOMOD_TYPES]
        )
        buf += '.'
        message.respond(buf)

    def __str__(self) -> str:
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Automoderation module: manages the automoderation functions. Commands: {', '.join(self.commands.keys())}"
