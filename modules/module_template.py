"""module_template.py
    serves as a template for the Module class to base other module files off of
    by Annika"""

from typing import Dict, Any
import core

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self) -> None:
        self.commands: Dict[str, Any] = {
            "command": self.exampleCommand, "alias": self.exampleCommand, "ping": self.exampleCommand
        }

    def exampleCommand(self, message: core.BotMessage) -> None:
        """Example command: replies "Pong!"

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        message.respond("Pong!")

    def __str__(self) -> str:
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Example module: provides an example for how to write modules. Commands: {', '.join(self.commands.keys())}"
