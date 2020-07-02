"""dummies.py
    helper classes for testing without a connection to Pokemon Showdown
    by Annika"""
import psclient
import core

# pylint: disable=super-init-not-called

class DummyConnection(core.BotConnection):
    """A modified version of Connection to be used for offline testing
    """
    def __init__(self, logchat=False):
        super().__init__()
        if logchat: self.chatlogger = psclient.chatlog.Chatlogger("chatlogging-test/")
        self.roomList = {
            core.BotRoom("testroom", self), core.BotRoom("testroom2", self),
            core.BotRoom("testroom3", self), core.BotRoom("lobby", self)
        }

    def send(self, message):
        """The send() method is disabled in DummyConnection
        """

class DummyMessage(core.BotMessage):
    """A modified version of Message to be used for offline testing
    """
    def __init__(
        self, sender=None, arguments=None, room=None, body=None, time=None,
        messageType=None, challstr=None, senderName=None, connection=DummyConnection()
    ):
        self.sender = sender
        self.arguments = arguments
        self.room = room
        self.body = body
        self.time = time
        self.type = messageType
        self.challstr = challstr
        self.senderName = senderName
        self.connection = connection
        self.response = None
        #                          (because HTML is an acronym)
        self.HTMLResponse = None # pylint: disable=invalid-name

    def respond(self, response):
        """Captures the response to a message

        Args:
            response (string): the response
        """
        self.response = response

    def respondHTML(self, html):
        """Captures the HTML response to a message

        Args:
            html (string): the HTML
        """
        self.HTMLResponse = html

class DummyUser(core.BotUser):
    """A modified version of User to be used for offline testing
    """
    def __init__(self, name="", connection=None, userid=None, isAdmin=False):
        self.id = userid
        self.admin = isAdmin
        if connection: super().__init__(name, connection)

    def can(self, action, room):
        """For DummyUsers, can() takes into account the admin attribute
        """
        return self.admin or super().can(action, room)
