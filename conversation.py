import data
import core
import random
import config

############ conversation.py ############
## Gives conversation-starting prompts ##
## by Annika                           ##
#########################################

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self):
        self.commands = {
            "fact": self.showSnippet, "topic": self.showSnippet, "addfact": self.addSnippet, "addtopic": self.addSnippet
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
            return message.respond("There are no " + ("facts" if isFact else "topics") + " for this room.")
        
        message.respond(random.choice(snippetList[roomid]))
    
    def addSnippet(self, message):
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
        snippetList = self.factList if isFact else self.topicList
        if not snippetList: snippetList = {room.id: []}
        if room.id not in snippetList.keys(): snippetList[room.id] = []

        if snippet not in snippetList[room.id]:
            snippetList[room.id].append(snippet)
            if isFact: 
                self.factList = snippetList
                data.store("factList", self.factList)
            else:
                self.topicList = snippetList
                data.store("topicList", self.topicList)
            return message.respond(("Fact" if isFact else "Topic") + " was successfully added!")
        else:
            return message.respond("That " + ("fact" if isFact else "topic") + " is already in the room's list!")


    
    def __str__(self):
        """String representation of the Module

        Returns:
            string -- representation
        """
        return "Conversation module: helps start conversations by displaying snippets. Commands: " + ", ".join(self.commands.keys())