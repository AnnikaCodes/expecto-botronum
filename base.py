import config
import core
import threading

########## base.py ###########
## contains the base module ##
## by Annika                ##
##############################

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self):
        self.commands = {"ping": self.ping, "owo": self.owo, "uwu": self.uwu, "eval": self.eval, "timer": self.timer}

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
            text = text.replace(vowel, (vowel + 'w' + vowel))
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
    
    def eval(self, message):
        """eval: evaluates the given Python expression

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if message.sender.isAdmin and message.sender.id in config.sysops:
            expression = config.separator.join(message.arguments[1:])
            try:
                response = str(eval(expression))
            except Exception as err:
              response = str(err)
        else:
            message.respond("Permission denied. This request has been logged.")
            core.log("W: base.eval(): eval permission denied for userid: " + message.sender.id)
            return
        response = "!code " + ("\n" if "\n" not in response else "") + response
        message.respond(response)

    def timer(self, message):
        """timer: evaluates the given Python expression

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if len(message.arguments) not in range(1,4):
            message.respond("Usage: ``" + config.commandCharacter + "timer <duration>, <optional message>``")
            return
        response = "/wall " if message.type == 'pm' or message.connection.bot.can('wall', message.room) else ""
        response += message.arguments[2] if len(message.arguments) > 2 else "Timer set by {user} is up".format(user = message.sender.name)
        duration = 5.0
        try:
            duration = float(message.arguments[1])
        except ValueError:
            message.respond(message.arguments[1] + " isn't a valid duration")
            return
        threading.Timer(duration, message.respond, args = [response]).start()

    def __str__(self):
        """String representation of the Module

        Returns:
            string -- representation
        """
        return "Base module: provides basic bot functionality. Commands: " + ", ".join(self.commands.keys())