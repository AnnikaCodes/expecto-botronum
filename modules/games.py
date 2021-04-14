"""games.py
    helps host games
    by Annika"""

from typing import Dict
import random
import psclient # type: ignore

import data
import config
import core

TOUR_SETUP_COMMANDS = [
    '/tour autostart 5',
    '/tour autodq 2',
    '/tour forcetimer on',
    '/tour modjoin disallow'
]

UNO_COMMANDS = [
    '/uno create 1000',
    '/uno timer 45',
    '/uno autostart 120'
]

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self) -> None:
        self.commands = {
            "reverse": self.reverse, "wallrev": self.reverse, "addreversioword": self.addReversioWord,
            "removereversioword": self.removeReversioWord, "rmreversioword": self.removeReversioWord,
            "addpoint": self.addPoints, "addpoints": self.addPoints, "deletereversioword": self.removeReversioWord,
            "showpoints": self.showLB, "lb": self.showLB, "showlb": self.showLB,
            "resetlb": self.resetLB, "lbreset": self.resetLB, "clearlb": self.resetLB, "lbclear": self.resetLB,
            "tour": self.startGame, "tournament": self.startGame, "uno": self.startGame
        }

        self.reversioWords = data.get("reversioWords")
        if not self.reversioWords:
            self.reversioWords = {}
            data.store("reversioWords", {})

        self.minigamePoints: Dict[str, dict] = {}

    def reverse(self, message: core.BotMessage) -> None:
        """Sends a reversed phrase for the Reversio game.

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if message.room:
            roomID = message.room.id
        elif message.arguments and len(message.arguments) > 1:
            roomID = psclient.toID(message.arguments[1])
        else:
            return message.respond("You must specify a room.")

        if roomID not in self.reversioWords.keys() or len(self.reversioWords[roomID]) < 1:
            return message.respond(f"There are no reversio words for the room {roomID}.")
        response = "/wall " if (not message.room) or message.sender.can("wall", message.room) else ""
        response += random.choice(self.reversioWords[roomID]).lower()[::-1].strip()
        return message.respond(response)

    def addReversioWord(self, message: core.BotMessage) -> None:
        """Adds a word to the reversio database.

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if len(message.arguments) < 2:
            return message.respond(
                f"Usage: ``{config.commandCharacter}addreversioword {'[room], ' if not message.room else ''}<word>``."
            )
        word = ",".join(message.arguments[1:])
        room = message.room

        if not room and len(message.arguments) > 2:
            room = message.connection.getRoom(message.arguments[1])
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

    def removeReversioWord(self, message: core.BotMessage) -> None:
        """Removes a word from the reversio database.

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if len(message.arguments) < 2:
            return message.respond(
                f"Usage: ``{config.commandCharacter}removereversioword {'[room], ' if not message.room else ''}<word>``."
            )
        word = ",".join(message.arguments[1:])
        room = message.room

        if not room and len(message.arguments) > 2:
            room = message.connection.getRoom(message.arguments[1])
            word = ",".join(message.arguments[2:])
        if not room:
            return message.respond("You must specify a valid room.")
        word = word.strip().lower()

        if message.sender.can("addfact", room):
            if room.id not in self.reversioWords.keys() or word not in self.reversioWords[room.id]:
                return message.respond(f"Word {word} not found in the Reversio database for {room.id}.")
            self.reversioWords[room.id].remove(word)
            data.store("reversioWords", self.reversioWords)
            return message.respond("Word removed!")

        return message.respond("Permission denied.")

    def addPoints(self, message: core.BotMessage) -> None:
        """Adds points to the minigame leaderboard

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if not message.room: return message.respond("You can only add points in a room.")
        if not message.sender.can("hostgame", message.room): return message.respond("Permission denied.")

        if len(message.arguments) < 2:
            return message.respond(
                f"Usage: ``{config.commandCharacter}addpoints [comma-separated list of users], [optional number of points]``."
            )
        usernames = message.arguments[1:]
        points = 1
        if len(usernames) > 1 and isInt(usernames[len(usernames) - 1].strip()):
            points = int(usernames.pop())

        if message.room.id not in self.minigamePoints.keys(): self.minigamePoints[message.room.id] = {}
        for name in usernames:
            userid = psclient.toID((name))
            if userid not in self.minigamePoints[message.room.id].keys():
                self.minigamePoints[message.room.id][userid] = points
            else:
                self.minigamePoints[message.room.id][userid] += points

        return message.respond("Points added!")

    def showLB(self, message: core.BotMessage) -> None:
        """Displays the minigame leaderboard

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        roomid = message.room.id if message.room else None
        if not roomid:
            if len(message.arguments) < 2: return message.respond("You must specify a room.")
            roomid = psclient.toID(message.arguments[1])
        if not roomid: return message.respond("You must specify a room.")
        if roomid not in self.minigamePoints.keys(): return message.respond("There are no scores.")

        points = self.minigamePoints[roomid]
        # TODO: investigate mypy errors
        sortedUsers = sorted(points, key=points.get, reverse=True) # type: ignore
        formattedPoints = ", ".join([f"{key} (**{points[key]}**)" for key in sortedUsers])
        return message.respond(f"**Scores**: {formattedPoints}" if formattedPoints else "There are no scores.")

    def resetLB(self, message: core.BotMessage) -> None:
        """Resets the minigame leaderboard

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        room = message.room
        if not room:
            if len(message.arguments) < 2: return message.respond("You must specify a room.")
            room = message.connection.getRoom(message.arguments[1])
        if not room: return message.respond("You must specify a room.")

        if not message.sender.can("hostgame", message.room): return message.respond("Permission denied.")
        if room.id not in self.minigamePoints.keys():
            return message.respond(f"There are no scores in the leaderboard for the room '{room.id}'.")

        del self.minigamePoints[room.id]
        return message.respond("Cleared the minigame leaderboard!")


    def startGame(self, message: core.BotMessage) -> None:
        """Starts a tournament or game of UNO

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if not message.room: return message.respond("You cannot start a game in PMs.")
        if not message.sender.can("hostgame", message.room): return message.respond("Permission denied.")
        isTournament = message.arguments[0].strip(config.commandCharacter) in ['tour', 'tournament']
        if isTournament and len(message.arguments) < 2: return message.respond(
            f"Usage: ``{config.commandCharacter}tournament [format], [comma-separated custom rules]``."
        )

        if isTournament:
            commands = TOUR_SETUP_COMMANDS
            tourFormat = message.arguments[1]
            rules = ', '.join(message.arguments[2:])
            message.room.say(f"/tour new {tourFormat},elim")
            message.room.say(f"/tour rules {rules}")
        else:
            commands = UNO_COMMANDS
        for command in commands:
            message.room.say(command)

    def __str__(self) -> str:
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Games module: assists with the hosting of games. Commands: {', '.join(self.commands.keys())}"

def isInt(string: str) -> bool:
    """Returns True if a string represents an integer and False otherwise.

    Arguments:
        string {str} -- the string

    Returns:
        bool -- whether or not the string is an integer
    """
    # Inspired by this StackOverflow question
    # https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
    return string[1:].isdigit() if string[0] == '-' else string.isdigit()
