"""logsearch.py
    handles searching chat logs
    by Annika"""

from typing import Dict, List
import html
import psclient # type: ignore

import config
import core

# 102400 is the maximum size of a message to the PS! servers; 19 is the maximum length of a username.
MAX_BUF_LEN = 102400 - 19 - len("/pminfobox ,") - len("</details>")

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self) -> None:
        self.commands = {"logsearch": self.logsearch, "searchlogs": self.logsearch}

    def logsearch(self, message: core.BotMessage) -> None:
        """Searches logs

        Args:
            message (message: core.BotMessage) -> None: the Message object that invoked the command
        """
        if len(message.arguments) < 2:
            return message.respond(f"Usage: ``{config.commandCharacter}logsearch <room>, [optional user], [optional keyword]``.")
        if not message.connection.chatlogger: return message.respond("There is currently no chatlogger loaded.")
        roomID = psclient.toID(message.arguments[1]).lower()
        userID = psclient.toID(message.arguments[2]).lower() if len(message.arguments) > 2 else ""
        keyword = ','.join(message.arguments[3:]).strip().lower() if len(message.arguments) > 3 else ""

        room = message.connection.getRoom(roomID)
        if not room: return message.respond(f"Invalid room: {roomID}")
        if not message.sender.can("searchlog", room): return message.respond("Permission denied.")

        resultsDict: Dict[str, List[str]] = message.connection.chatlogger.search(roomID=roomID, userID=userID, keyword=keyword)
        days: List[str] = list(resultsDict.keys())
        days.sort(reverse=True)
        summary = f"Chatlogs in {html.escape(roomID)} from {html.escape(userID) if userID else 'any user'}"
        if keyword: summary += f" matching the keyword <code>{html.escape(keyword)}</code>"

        htmlBuf = f"<details><summary>{summary}</summary>"
        for day in days:
            attemptedBuf = f'<details style="margin-left: 5px;"><summary>{day}</summary><div style="margin-left: 10px;">'
            attemptedBuf += "<br />".join([
                message.connection.chatlogger.formatData(result, isHTML=True) for result in resultsDict[day]
            ])
            attemptedBuf += "</div></details>"
            if len(htmlBuf) + len(attemptedBuf) < MAX_BUF_LEN:
                htmlBuf += attemptedBuf
            else:
                break

        htmlBuf += "</details>"
        return message.respondHTML(htmlBuf)

    def __str__(self) -> str:
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Logsearch module: handles searching chatlogs. Commands: {', '.join(self.commands.keys())}"
