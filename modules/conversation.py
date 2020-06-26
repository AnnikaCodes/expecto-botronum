import data
import core
import random
import config
from pbwrap import Pastebin

############ conversation.py ############
## Gives conversation-starting prompts ##
## by Annika                           ##
#########################################

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self):
        self.commands = {
            "fact": self.showSnippet, "topic": self.showSnippet, "addfact": self.manageSnippet, 
            "addtopic": self.manageSnippet, "deletefact": self.manageSnippet, "removefact": self.manageSnippet,
            "deletetopic": self.manageSnippet, "removetopic": self.manageSnippet, "countfacts": self.countSnippets,
            "factcount": self.countSnippets, "counttopics": self.countSnippets, "topiccount": self.countSnippets,
            "factlist": self.exportSnippets, "listfacts": self.exportSnippets, "topiclist": self.exportSnippets,
            "listtopics": self.exportSnippets
        }
        self.factList = data.get("factList")
        self.topicList = data.get("topicList")

    def showSnippet(self, message):
        """Shows a fact or topic in chat

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        isFact = "fact" in message.arguments[0]
        snippetList = self.factList if isFact else self.topicList
        if message.room:
            roomid = message.room.id
        elif len(message.arguments) > 1:
            roomid = core.toID(message.arguments[1])
        else:
            return message.respond("You must specify a room.")

        if not snippetList or roomid not in snippetList.keys():
            return message.respond(f"There are no {'facts' if isFact else 'topics'} for this room.")
        
        message.respond(random.choice(snippetList[roomid]))
    
    def manageSnippet(self, message):
        """Removes or adds a fact or topic

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if message.room and len(message.arguments) > 1:
            room = message.room
            snippet = ",".join(message.arguments[1:]).strip()
        elif len(message.arguments) > 2:
            room = message.connection.getRoomByName(message.arguments[1])
            snippet = ",".join(message.arguments[2:]).strip()
        else:
            return message.respond("You must specify a fact/topic (and a room if used in PMs).")

        if not message.sender.can("addfact", room): return message.respond("Permission denied.")
        isFact = "fact" in message.arguments[0]
        isAddition = "add" in message.arguments[0]
        snippetList = self.factList if isFact else self.topicList
        if not snippetList: snippetList = {room.id: []}
        if room.id not in snippetList.keys(): snippetList[room.id] = []

        if snippet not in snippetList[room.id] and isAddition:
            snippetList[room.id].append(snippet)
            message.respond(f"{'Fact' if isFact else 'Topic'} was successfully added!")
        elif snippet in snippetList[room.id] and not isAddition:
            snippetList[room.id].remove(snippet)
            message.respond(f" was successfully removed!")
        else:
            return message.respond(f"That {'Fact' if isFact else 'Topic'} is \
                {'already' if isAddition else 'not'} in the room's list!")

        if isFact: 
            self.factList = snippetList
            data.store("factList", self.factList)
        else:
            self.topicList = snippetList
            data.store("topicList", self.topicList)

    def countSnippets(self, message):
        """Counts the number of snippets

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        isFact = "fact" in message.arguments[0]
        snippetList = self.factList if isFact else self.topicList
        if message.room:
            room = message.room
        elif len(message.arguments) > 1:
            room = message.connection.getRoomByName(message.arguments[1])
        else:
            return message.respond("You must specify a room.")
        
        num = 0
        if snippetList and room.id in snippetList.keys(): num = len(snippetList[room.id])
        return message.respond(f"There {'is ' if num == 1 else 'are '} {str(num)} \
            {'fact' if isFact else 'topic'}{'' if num == 1 else 's'} for the room {room.id}.")
    
    def exportSnippets(self, message):
        """Exports the snippets to Pastebin

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        isFact = "fact" in message.arguments[0]
        snippetList = self.factList if isFact else self.topicList
        if message.room:
            room = message.room
        elif len(message.arguments) > 1:
            room = message.connection.getRoomByName(message.arguments[1])
        else:
            return message.respond("You must specify a room.")
        if not message.sender.can("addfact", room): return message.respond("Permission denied.")
        if room.id not in snippetList.keys() or len(snippetList[room.id]) == 0: 
            return message.respond(f"There are no {'facts' if isFact else 'topics'} for the room {room.id}.")

        pasteData = "\n".join(snippetList[room.id])
        return message.respond(str(Pastebin(config.pastebinAPIKey).create_paste(
            pasteData, # the data
            1, # unlisted paste
            f"{'Facts' if isFact else 'Topics'} for room {room.id}" # title
        )))

    def __str__(self):
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Conversation module: helps start conversations by displaying snippets. Commands: {', '.join(self.commands.keys())}"