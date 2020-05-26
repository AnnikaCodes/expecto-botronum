import config
import core

########## base.py ###########
## contains the base module ##
## by Annika                ##
##############################

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self):
        self.commands = {"ping": self.ping, "owo": self.owo, "uwu": self.uwu, "eval": self.eval}

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

    def __str__(self):
        """String representation of the Module

        Returns:
            string -- representation
        """
        return "Base module: provides basic bot functionality. Commands: " + ", ".join(self.commands.keys())