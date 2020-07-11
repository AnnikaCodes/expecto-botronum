"""houses.py

    tracks users' Harry Potter houses

    by Annika"""

from typing import Dict, Any, List

import psclient # type: ignore

import core
import config
import data

def getUserHouses(userid: str) -> List[str]:
    """Fetches a list of houses a user is in

    Args:
        userid (str): the user's ID

    Returns:
        List[str]: a list of houses
    """
    houseData: Dict[str, list] = data.get("houses") or {}
    return [house for house in houseData if userid in houseData[house]]

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self) -> None:
        self.commands: Dict[str, Any] = {
            "checkhouse": self.checkHouse, "house": self.checkHouse, "joinhouse": self.joinHouse, "join": self.joinHouse,
            "createhouse": self.createHouse, "newhouse": self.createHouse
        }

    def checkHouse(self, message: core.BotMessage) -> None:
        """Checks what house a user is in

        Arguments:
            message (core.Botmessage: core.BotMessage) -> None: the Message object that invoked the command
        """
        user: str = ','.join(message.arguments[1:]) if len(message.arguments) > 1 else message.senderName
        houses: List[str] = getUserHouses(psclient.toID(user))
        if houses: return message.respond(f"{user} is in {houses[0].title()} house!")
        return message.respond(f"{user} is not in any house.")

    def joinHouse(self, message: core.BotMessage) -> None:
        """Joins a house

        Args:
            message (core.Botmessage: core.BotMessage) -> None: the message that invoked the command
        """
        if not message.sender.id: return message.respond("Only users can join houses.") # Shouldn't happen
        if len(message.arguments) < 2: return message.respond(f"Usage: ``{config.commandCharacter}joinhouse <house>``")
        house: str = psclient.toID(','.join(message.arguments[1:]))
        houseData: Dict[str, list] = data.get("houses") or {}
        if house not in houseData:
            return message.respond(f"{house.title()} is not a known house. Try one of: {', '.join(list(houseData.keys()))}")
        currentHouses: List[str] = getUserHouses(message.sender.id)
        for oldHouse in currentHouses:
            houseData[oldHouse].remove(message.sender.id)
        houseData[house].append(message.sender.id)
        data.store("houses", houseData)
        leaveMessage = f" left {', '.join([house.title() for house in currentHouses])} and" if currentHouses else ""
        return message.respond(
            f"Successfully{leaveMessage} joined {house.title()}!"
        )

    def createHouse(self, message: core.BotMessage) -> None:
        """Creates a new house

        Args:
            message (core.Botmessage: core.BotMessage) -> None: the message that invoked the command
        """
        if message.sender.id not in config.sysops:
            return message.respond(
                f"Only bot operators (sysops) can create houses. The bot operators are: {', '.join(config.sysops)}"
            )
        if len(message.arguments) < 2: return message.respond(f"Usage: ``{config.commandCharacter}createhouse <house>``")
        house: str = psclient.toID(','.join(message.arguments[1:]))
        houseData: Dict[str, list] = data.get("houses") or {}
        if house in houseData: return message.respond(f"The house {house} already exists. Houses can only be deleted manually.")
        houseData[house] = []
        data.store("houses", houseData)
        return message.respond(f"Successfully created the house {house.title()}!")

    def __str__(self) -> str:
        """String representation of the Module

        Returns:
            string: representation
        """
        return f"Houses module: tracks users' Harry Potter houses. Commands: {', '.join(self.commands.keys())}"
