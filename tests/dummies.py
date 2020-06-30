"""message_capture.py
    helpers for testing messages
    by Annika"""
import core

# pylint: disable=super-init-not-called

class DummyConnection(core.Connection):
    """A modified version of Connection to be used for offline testing
    """
    def __init__(self):
        super().__init__()
        self.roomList = {
            core.Room("testroom", self), core.Room("testroom2", self),
            core.Room("testroom3", self), core.Room("lobby", self)
        }

    def send(self, message):
        """The send() method is disabled in DummyConnection
        """

class DummyMessage(core.Message):
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
        self.HTMLResponse = None

    def respond(self, response):
        """Captures the response to a message

        Args:
            response (string): the response
        """
        self.response = response

    def respondHTML(self, response):
        """Captures the HTML response to a message

        Args:
            response (string): the HTML
        """
        self.HTMLResponse = response

class DummyUser(core.User):
    """A modified version of User to be used for offline testing
    """
    def __init__(self, userid=None, isAdmin=False):
        self.id = userid
        self.isAdmin = isAdmin
