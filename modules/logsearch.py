import config
import core

import html

########## logsearch.py #########
## Handles searching chat logs ##
## by Annika                   ##
#################################

# 102400 is the maximum size of a message to the PS! servers; 19 is the maximum length of a username.
MAX_BUF_LEN = 102400 - 19 - len("/pminfobox ,") - len("</details>")

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self):
        self.commands = {"logsearch": self.logsearch, "searchlogs": self.logsearch}

    def logsearch(self, message):
        """Searches logs

        Args:
            message (Message): the Message object that invoked the command
        """
        if len(message.arguments) < 2: return message.respond(
            "Usage: ``{char}logsearch <room>, [optional user], [optional keyword(s)]``.".format(char = config.commandCharacter)
        )
        roomid = core.toID(message.arguments[1]).lower()
        userid = core.toID(message.arguments[2]).lower() if len(message.arguments) > 2 else ""
        keywords = ','.join(message.arguments[3:]).lower() if len(message.arguments) > 3 else ""

        room = message.connection.getRoomByID(roomid)
        if not room: return message.respond("Invalid room: " + roomid)
        if not message.sender.can("searchlog", room): return message.respond("Permission denied.")

        resultsDict = message.connection.chatlogger.search(roomid = roomid, userid = userid, keyword = keywords)

        summary = "Chatlogs{query} in {room} from {user}".format(
            query = " for " + html.escape(keywords) if keywords else "",
            room = html.escape(roomid),
            user = html.escape(userid) if userid else "any user"
        )
        htmlBuf = "<details><summary>{summary}</summary>".format(summary = summary)
        for day in resultsDict.keys():
            attemptedBuf = '<details style="margin-left: 5px;"><summary>' + day + '</summary><div style="margin-left: 10px;">'
            attemptedBuf += "<br />".join([message.connection.chatlogger.formatData(result, isHTML = True) for result in resultsDict[day]])
            attemptedBuf += "</div></details>"
            if len(htmlBuf) + len(attemptedBuf) < MAX_BUF_LEN:
                htmlBuf += attemptedBuf
            else:
                break
        htmlBuf += "</details>"
        message.respondHTML(htmlBuf)

    def __str__(self):
        """String representation of the Module

        Returns:
            string -- representation
        """
        return "Logsearch module: handles searching chatlogs. Commands: " + ", ".join(self.commands.keys())
