"""dummies.py
    helper classes for testing without a connection to Pokemon Showdown
    by Annika"""

from typing import Optional, List
import psclient # type: ignore
import core
import chatlog

# pylint: disable=super-init-not-called

class DummyConnection(core.BotConnection):
    """A modified version of Connection to be used for offline testing
    """
    def __init__(self, logchat: bool = False) -> None:
        super().__init__()
        if logchat:
            self.chatlogger = chatlog.Chatlogger(":memory:")
            #try:
            self.chatlogger.SQL.executescript(open('log-schema.sql').read())
            # except:
            #     pass
        self.roomList = {
            core.BotRoom("testroom", self), core.BotRoom("testroom2", self),
            core.BotRoom("testroom3", self), core.BotRoom("lobby", self)
        }

    def send(self, message: core.BotMessage) -> None:
        """The send() method is disabled in DummyConnection
        """

class DummyMessage(core.BotMessage):
    """A modified version of Message to be used for offline testing
    """
    def __init__(
        self, sender: str = None, arguments: List[str] = None, room: psclient.Room = None, body: str = None,
        time: str = None, messageType: str = None, challstr: str = None, senderName: str = None,
        connection: psclient.PSConnection = DummyConnection()
    ) -> None:
        self.sender = sender
        if arguments: self.arguments = arguments
        self.room = room
        self.body = body
        self.time = time
        self.type = messageType
        self.challstr = challstr
        self.senderName = senderName
        self.connection = connection
        self.response: Optional[str] = None
        #                          (because HTML is an acronym)
        self.HTMLResponse: Optional[str] = None # pylint: disable=invalid-name

    def respond(self, response: str) -> None:
        """Captures the response to a message

        Args:
            response (string): the response
        """
        self.response = response

    def respondHTML(self, html: str) -> None:
        """Captures the HTML response to a message

        Args:
            html (string): the HTML
        """
        self.HTMLResponse = html

class DummyUser(core.BotUser):
    """A modified version of User to be used for offline testing
    """
    def __init__(self,
        name: str = "",
        connection: psclient.PSConnection = None,
        userid: str = None,
        isAdmin: bool = False
    ) -> None:
        self.id = userid
        self.admin = isAdmin
        if connection: super().__init__(name, connection)

    def can(self, action: str, room: psclient.Room) -> bool:
        """For DummyUsers, can() takes into account the admin attribute
        """
        return self.admin or super().can(action, room)
