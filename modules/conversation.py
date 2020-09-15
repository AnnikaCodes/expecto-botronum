"""conversation.py
    manages snippets to give conversation-starting prompts in chat
    by Annika"""

import random
import re
import psclient # type: ignore
from pbwrap import Pastebin # type: ignore

import data
import config
import core

class Module:
    """Represents a module, which may contain several commands
    """
    def __init__(self) -> None:
        self.commands = {
            "fact": self.showSnippet, "facc": self.showSnippet, "topic": self.showSnippet, "quote": self.showSnippet,
            "addfact": self.manageSnippet, "addtopic": self.manageSnippet, "addquote": self.manageSnippet,
            "deletefact": self.manageSnippet, "removefact": self.manageSnippet,
            "deletetopic": self.manageSnippet, "removetopic": self.manageSnippet,
            "deletequote": self.manageSnippet, "removequote": self.manageSnippet,
            "countfacts": self.countSnippets, "factcount": self.countSnippets,
            "counttopics": self.countSnippets, "topiccount": self.countSnippets,
            "countquotes": self.countSnippets, "quotecount": self.countSnippets,
            "factlist": self.exportSnippets, "listfacts": self.exportSnippets,
            "topiclist": self.exportSnippets, "listtopics": self.exportSnippets,
            "quotelist": self.exportSnippets, "listquotes": self.exportSnippets
        }
        self.factList = data.get("factList")
        self.topicList = data.get("topicList")
        self.quoteList = data.get("quoteList")

    def showSnippet(self, message: core.BotMessage) -> None:
        """Shows a fact, quote, or topic in chat

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        kind = 'facts'
        snippetList = self.factList
        if "topic" in message.arguments[0]:
            kind = 'topics'
            snippetList = self.topicList
        elif "quote" in message.arguments[0]:
            kind = 'quotes'
            snippetList = self.quoteList

        if message.room:
            roomid = message.room.id
        elif len(message.arguments) > 1:
            roomid = psclient.toID(message.arguments[1])
        else:
            return message.respond("You must specify a room.")

        if not snippetList or roomid not in snippetList.keys():
            return message.respond(f"There are no {kind} for this room.")

        return message.respond(random.choice(snippetList[roomid]))

    def manageSnippet(self, message: core.BotMessage) -> None:
        """Removes or adds a fact, topic, or quote

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        if message.room and len(message.arguments) > 1:
            room = message.room
            snippet = ",".join(message.arguments[1:]).strip()
        elif len(message.arguments) > 2:
            room = message.connection.getRoom(message.arguments[1])
            snippet = ",".join(message.arguments[2:]).strip()
        else:
            return message.respond("You must specify a fact/topic/quote (and a room if used in PMs).")

        if not message.sender.can("addfact", room): return message.respond("Permission denied.")
        if not re.match(r'[a-zA-Z0-9]', snippet): snippet = " " + snippet

        kind = 'Fact'
        snippetList = self.factList
        if "topic" in message.arguments[0]:
            kind = 'Topic'
            snippetList = self.topicList
        elif "quote" in message.arguments[0]:
            kind = 'Quote'
            snippetList = self.quoteList
        isAddition = "add" in message.arguments[0]

        if not snippetList: snippetList = {room.id: []}
        if room.id not in snippetList.keys():
            snippetList[room.id] = []

        if snippet not in snippetList[room.id] and isAddition:
            snippetList[room.id].append(snippet)
            message.respond(f"{kind} was successfully added!")
        elif snippet in snippetList[room.id] and not isAddition:
            snippetList[room.id].remove(snippet)
            message.respond(f"{kind} was successfully removed!")
        else:
            return message.respond(f"That {kind} is {'already' if isAddition else 'not'} in the room's list!")

        if kind == 'Topic':
            self.topicList = snippetList
            return data.store("topicList", self.topicList)
        if kind == 'Quote':
            self.quoteList = snippetList
            return data.store("quoteList", self.quoteList)
        self.factList = snippetList
        return data.store("factList", self.factList)

    def countSnippets(self, message: core.BotMessage) -> None:
        """Counts the number of snippets

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        kind = 'fact'
        snippetList = self.factList
        if "topic" in message.arguments[0]:
            kind = 'topic'
            snippetList = self.topicList
        elif "quote" in message.arguments[0]:
            kind = 'quote'
            snippetList = self.quoteList

        if message.room:
            room = message.room
        elif len(message.arguments) > 1:
            room = message.connection.getRoom(message.arguments[1])
        else:
            return message.respond("You must specify a room.")

        num = 0
        if snippetList and room.id in snippetList.keys(): num = len(snippetList[room.id])
        return message.respond(f"There {'is ' if num == 1 else 'are '} {str(num)} \
            {kind}{'' if num == 1 else 's'} for the room {room.id}.")

    def exportSnippets(self, message: core.BotMessage) -> None:
        """Exports the snippets to Pastebin

        Arguments:
            message {Message} -- the Message object that invoked the command
        """
        kind = 'fact'
        snippetList = self.factList
        if "topic" in message.arguments[0]:
            kind = 'topic'
            snippetList = self.topicList
        elif "quote" in message.arguments[0]:
            kind = 'quote'
            snippetList = self.quoteList

        if message.room:
            room = message.room
        elif len(message.arguments) > 1:
            room = message.connection.getRoom(message.arguments[1])
        else:
            return message.respond("You must specify a room.")
        if not message.sender.can("addfact", room): return message.respond("Permission denied.")
        if room.id not in snippetList.keys() or len(snippetList[room.id]) == 0:
            return message.respond(f"There are no {kind}s for the room {room.id}.")

        pasteData = "\n".join(snippetList[room.id])
        return message.respond(str(Pastebin(config.pastebinAPIKey).create_paste(
            pasteData, # the data
            1, # unlisted paste
            f"{kind.title()}s for room {room.id}" # title
        )))

    def __str__(self) -> str:
        """String representation of the Module

        Returns:
            string -- representation
        """
        return f"Conversation module: displays snippets of text in chat. Commands: {', '.join(self.commands.keys())}"
