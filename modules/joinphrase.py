"""joinphrase.py
    handles adding and removing joinphrases
    by Annika"""

import psclient
import config

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self):
        self.commands = {
            "addjoinphrase": self.addJP, "addjp": self.addJP, "removejoinphrase": self.deleteJP, "removejp": self.deleteJP,
            "deletejoinphrase": self.deleteJP, "deletejp": self.deleteJP
        }

    def addJP(self, message):
        """Adds a joinphrase for a user

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        phrase = ""
        userid = ""
        if message.room:
            room = message.room
            if len(message.arguments) > 2:
                userid = psclient.toID(message.arguments[1])
                phrase = ",".join(message.arguments[2:]).strip()
        elif len(message.arguments) > 3:
            room = message.connection.getRoom(message.arguments[1])
            userid = psclient.toID(message.arguments[2])
            phrase = ",".join(message.arguments[3:])
        else:
            return message.respond("You must specify a room.")
        if not phrase or not userid:
            return message.respond(
                f"Usage: ``{config.commandCharacter}addjoinphrase {'[room], ' if not message.room else ''}[user], [phrase]``. "
            )
        if not message.sender.can("manage", room): return message.respond("Permission denied.")

        room.addJoinphrase(phrase, userid)
        return message.respond("Joinphrase successfully added!")

    def deleteJP(self, message):
        """Removes a joinphrase for a user

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        userid = ""
        if message.room:
            room = message.room
            if len(message.arguments) > 1:
                userid = psclient.toID(message.arguments[1])
        elif len(message.arguments) > 2:
            room = message.connection.getRoom(message.arguments[1])
            userid = psclient.toID(message.arguments[2])
        else:
            return message.respond("You must specify a room.")
        if not userid:
            return message.respond(
                f"Usage: ``{config.commandCharacter}removejoinphrase {'[room], ' if not message.room else ''}[user]``. "
            )
        if not message.sender.can("manage", room): return message.respond("Permission denied.")

        room.removeJoinphrase(userid)
        return message.respond("Joinphrase successfully removed!")


    def __str__(self):
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Joinphrase module: handles joinphrases. Commands: {' ,'.join(self.commands.keys())}"
