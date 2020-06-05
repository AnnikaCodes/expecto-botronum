import config
import core

########## logsearch.py #########
## Handles searching chat logs ##
## by Annika                   ##
#################################

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
        roomid = core.toID(message.arguments[1])
        userid = core.toID(message.arguments[2]) if len(message.arguments) > 2 else ""
        keywords = ','.join(message.arguments[3:]) if len(message.arguments) > 3 else ""

        room = message.connection.getRoomByID(roomid)
        if not room: return message.respond("Invalid room: " + roomid)
        if not message.sender.can("searchlog", room): return message.respond("Permission denied.")

        resultsDict = message.connection.chatlogger.search(roomid = roomid, userid = userid, keyword = keywords)

        summary = "Chatlogs{query} in {room} from {user}".format(
            query = " for " + keywords if keywords else "",
            room = roomid,
            user = userid if userid else "any user"
        )
        htmlBuf = "<details><summary>{summary}</summary>".format(summary = summary)
        for day in resultsDict.keys():
            htmlBuf += "<details><summary>" + day + "</summary>"
            htmlBuf += "<br />".join([core.escapeHTML(message.connection.chatlogger.formatData(result)) for result in resultsDict[day]])
            htmlBuf += "</details>"
        htmlBuf += "</details>"
        core.log("DEBUG: " + htmlBuf)
        message.respondHTML(htmlBuf)

    def __str__(self):
        """String representation of the Module

        Returns:
            string -- representation
        """
        return "Logsearch module: handles searching chatlogs. Commands: " + ", ".join(self.commands.keys())
