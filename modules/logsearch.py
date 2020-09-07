"""logsearch.py
    handles searching chat logs
    by Annika"""

## TODO: Convert this to a database
## SQLite? Postgres? idk, but flat files suck

from typing import Dict, List
import html
from datetime import datetime

import psclient # type: ignore

import config
import core

# 102400 is the maximum size of a message to the PS! servers; 19 is the maximum length of a username.
MAX_BUF_LEN = 102400 - 19 - len("/pminfobox ,") - len("</details>")
TOPUSERS = 50

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self) -> None:
        self.commands = {
            "logsearch": self.logsearch, "searchlogs": self.logsearch,
            "linecount": self.linecount, "topusers": self.topusers
        }

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
            daySummary = f"{day} ({len(resultsDict[day])} match{'es' if len(resultsDict[day]) != 1 else ''})"
            attemptedBuf = f'<details style="margin-left: 5px;"><summary>{daySummary}</summary><div style="margin-left: 10px;">'
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

    def linecount(self, message: core.BotMessage) -> None:
        """Gets a user's linecount

        Args:
            message (message: core.BotMessage) -> None: the Message object that invoked the command
        """
        if len(message.arguments) < 3:
            return message.respond(f"Usage: ``{config.commandCharacter}linecount <user>, <room>, [optional number of days]``.")

        userID = psclient.toID(message.arguments[1])
        roomID = psclient.toID(message.arguments[2])
        try:
            days = int(message.arguments[3])
        except (IndexError, ValueError):
            days = 30

        room = message.connection.getRoom(roomID)
        if not message.connection.chatlogger: return message.respond("There is currently no chatlogger loaded.")
        if not room: return message.respond(f"Invalid room: {roomID}")
        if not message.sender.can("searchlog", room): return message.respond("Permission denied.")

        resultsDict: Dict[str, List[str]] = message.connection.chatlogger.search(roomID=roomID, userID=userID)
        dayResults: List[str] = list(resultsDict.keys())
        dayResults.sort(reverse=True)

        # TODO: make this less hacky and do it properly in ps-client
        oldestDay = str(datetime.fromtimestamp((datetime.now().timestamp() - days * 24 * 60 * 60)).date())
        dayResults = [result for result in dayResults if result >= oldestDay]

        count = 0
        details = []
        for result in dayResults:
            dayCount = len(resultsDict[result])
            count += dayCount
            details.append(f"<li>{result} — <strong>{dayCount}</strong> lines</li>")

        htmlBuf = f"The user <strong><code>{userID}</code></strong> had <strong>{count}</strong> lines \
            in the room {roomID} in the past {days} days!"
        htmlBuf += f"<details><summary>Linecounts per day</summary><ul>{''.join(details)}</ul></details>"
        return message.respondHTML(htmlBuf)

    def topusers(self, message: core.BotMessage) -> None:
        """Gets the top users of a room

        Args:
            message (message: core.BotMessage) -> None: the Message object that invoked the command
        """
        if len(message.arguments) < 2:
            return message.respond(f"Usage: ``{config.commandCharacter}topusers <room>, [optional number of days]``.")

        roomID = psclient.toID(message.arguments[1])
        try:
            days = int(message.arguments[2])
        except (IndexError, ValueError):
            days = 30

        room = message.connection.getRoom(roomID)
        if not message.connection.chatlogger: return message.respond("There is currently no chatlogger loaded.")
        if not room: return message.respond(f"Invalid room: {roomID}")
        if not message.sender.can("searchlog", room): return message.respond("Permission denied.")

        resultsDict: Dict[str, List[str]] = message.connection.chatlogger.search(roomID=roomID)
        dayResults: List[str] = list(resultsDict.keys())
        dayResults.sort(reverse=True)

        # TODO: make this less hacky and do it properly in ps-client
        oldestDay = str(datetime.fromtimestamp((datetime.now().timestamp() - days * 24 * 60 * 60)).date())
        dayResults = [result for result in dayResults if result >= oldestDay]

        users = {}
        for result in dayResults:
            for line in resultsDict[result]:
                userid = line.split('|')[0]
                if not userid: continue
                if userid not in users:
                    users[userid] = 1
                else:
                    users[userid] += 1

        sortedUsers = sorted(users, key=users.__getitem__, reverse=True)

        htmlBuf = f"<details><summary>Top {TOPUSERS} users in the room {roomID} in the past {days} days</summary><ul>"
        i = 0
        for user in sortedUsers:
            i += 1
            if i > TOPUSERS: break
            htmlBuf += f"<li><strong>{user}</strong> — {users[user]} lines</li>"
        htmlBuf += "</ul></details>"
        return message.respondHTML(htmlBuf)

    def __str__(self) -> str:
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Logsearch module: handles searching chatlogs. Commands: {', '.join(self.commands.keys())}"
