"""base.py
    contains the base module
    by Annika"""

import threading
import config

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self):
        self.commands = {"ping": self.ping, "owo": self.owo, "uwu": self.uwu, "timer": self.timer}

    def ping(self, message):
        """Ping: replies "Pong!"

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        message.respond("Pong!")

    def owo(self, message):
        """owo: replaces vowels with owo faces

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        text = config.separator.join(message.arguments[1:])
        for vowel in list("AaEeIiOoUu"):
            text = text.replace(vowel, f"{vowel}w{vowel}")
        message.respond(text)


    def uwu(self, message):
        """uwu: turns English into weird anime language

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        text = config.separator.join(message.arguments[1:])
        uwuRules = {'r': 'w', 'l': 'w', 'R': 'W', 'L': 'W'}
        for key in uwuRules:
            text = text.replace(key, uwuRules[key])
        message.respond(text)

    def timer(self, message):
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
        threading.Timer(duration, message.respond, args=[response]).start()

    def __str__(self):
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Base module: provides basic bot functionality. Commands: {', '.join(self.commands.keys())}"
