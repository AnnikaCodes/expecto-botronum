import random

import data
import config
import core

###### games.py ######
## Helps host games ##
## by Annika        ##
######################

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self):
        self.commands = {
            "reverse": self.reverse, "wallrev": self.reverse, "addreversioword": self.addReversioWord,
            "removereversioword": self.removeReversioWord, "rmreversioword": self.removeReversioWord,
            "deletereversioword": self.removeReversioWord
        }
        
        self.reversioWords = data.get("reversioWords")
        if not self.reversioWords:
            self.reversioWords = {}
            data.store("reversioWords", {})
    
    def reverse(self, message):
        """Sends a reversed phrase for the Reversio game.

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if message.room:
            roomID = message.room.id
        elif message.arguments and len(message.arguments) > 1:
            roomID = core.toID(message.arguments[1])
        else:
            return message.respond("You must specify a room.")

        if roomID not in self.reversioWords.keys() or len(self.reversioWords[roomID]) < 1:
            return message.respond("There are no reversio words for the room " + roomID + ".")
        response = "/wall " if (not message.room) or message.sender.can("wall", message.room) else ""
        response += random.choice(self.reversioWords[roomID]).lower()[::-1].strip()
        message.respond(response)
    
    def addReversioWord(self, message):
        """Adds a word to the reversio database.

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if len(message.arguments) < 2:
            return message.respond("Usage: ``" + config.commandCharacter + "addreversioword [room, if used in PMs], <word>``.")
        word = ",".join(message.arguments[1:])
        room = message.room

        if not room and len(message.arguments) > 2:
            room = message.connection.getRoomByName(message.arguments[1])
            word = ",".join(message.arguments[2:])
        if not room:
            return message.respond("You must specify a valid room.")
        word = word.strip().lower()

        if message.sender.can("addfact", room):
            if room.id not in self.reversioWords.keys():
                self.reversioWords[room.id] = [word]
            else:
                self.reversioWords[room.id].append(word)
            data.store("reversioWords", self.reversioWords)
            return message.respond("Word added!")
        
        return message.respond("Permission denied.")
    
    def removeReversioWord(self, message):
        """Removes a word from the reversio database.

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if len(message.arguments) < 2:
            return message.respond("Usage: ``" + config.commandCharacter + "removereversioword [room, if used in PMs], <word>``.")
        word = ",".join(message.arguments[1:])
        room = message.room

        if not room and len(message.arguments) > 2:
            room = message.connection.getRoomByName(message.arguments[1])
            word = ",".join(message.arguments[2:])
        if not room:
            return message.respond("You must specify a valid room.")
        word = word.strip().lower()
        
        if message.sender.can("addfact", room):
            if room.id not in self.reversioWords.keys() or word not in self.reversioWords[room.id]:
                return message.respond("Word {word} not found in the Reversio database for {room}.".format(
                    word = word,
                    room = room.id
                ))
            else:
                self.reversioWords[room.id].remove(word)
                data.store("reversioWords", self.reversioWords)
                return message.respond("Word removed!")
        
        return message.respond("Permission denied.")


    def __str__(self):
        """String representation of the Module

        Returns:
            string -- representation
        """
        return "Games module: assists with the hosting of games. Commands: " + ", ".join(self.commands.keys())