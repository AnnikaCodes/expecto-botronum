"""test_core.py
    tests for core
    by Annika"""

# pylint: disable=line-too-long

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).joinpath("../..").resolve()) + '/')

import core # pylint: disable=wrong-import-position

## Helper Classes ##
class DryRunConnection(core.Connection):
    """A modified version of Connection to be used for offline testing
    """
    def __init__(self):
        super().__init__()
        self.roomList = {
            core.Room("testroom", self), core.Room("testroom2", self),
            core.Room("testroom3", self), core.Room("lobby", self)
        }

    def send(self, message):
        """The send() method is disabled in DryRunConnection
        """

## Tests for Message objects ##
def testMessageChallstr():
    """Tests the ability of Message objects to handle challstrs
    """
    message = core.Message(
        "|challstr|4|314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823",
        DryRunConnection()
    )
    assert message.challstr == "4|314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823"

def testMessageChat():
    """Tests the ability of Message objects to parse chat messages including strange characters, from the Lobby
    """
    message = core.Message(
        "|c|#Ann/ika ^_^|Hi, I wrote a Python test|Isn't it cool?it,contains,odd characters och konstigt bokstaver från andra språk.",
        DryRunConnection()
    )
    assert message.senderName == "#Ann/ika ^_^"
    assert message.sender.id == "annika"
    assert message.arguments == ['Hi,', "I wrote a Python test|Isn't it cool?it", "contains", "odd characters och konstigt bokstaver från andra språk."]
    assert message.room.id == "lobby"
    assert message.body == "Hi, I wrote a Python test|Isn't it cool?it,contains,odd characters och konstigt bokstaver från andra språk."
    assert message.time is None
    assert message.type == 'chat'
    assert message.challstr is None
    assert isinstance(str(message), str)

def testMessageChatCommand():
    """Tests the ability of Message objects to handle commands sent to rooms, with arguments
    """
    message = core.Message(
        """>testroom
|c:|1593475694|#Ann/ika ^_^|~somecommand argument1,argumENT2||withpipes, argumént3""",
        DryRunConnection()
    )
    assert message.senderName == "#Ann/ika ^_^"
    assert message.sender.id == "annika"
    assert message.arguments == ["~somecommand", "argument1", "argumENT2||withpipes", " argumént3"]
    assert message.room.id == "testroom"
    assert message.body == "~somecommand argument1,argumENT2||withpipes, argumént3"
    assert message.time == "1593475694"
    assert message.type == 'chat'
    assert message.challstr is None


def testMessageJoin():
    """Tests the ability of Message objects to handle join messages
    """
    connection = DryRunConnection()
    message = core.Message(
        """>testroom
|J|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "join"
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))

    message = core.Message(
        """>testroom2
|j|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "join"
    assert 'testroom2' in connection.getUserRooms(connection.getUser('annika'))

    message = core.Message(
        """>testroom3
|join|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "join"
    assert 'testroom3' in connection.getUserRooms(connection.getUser('annika'))

def testMessageLeave():
    """Tests the ability of Message objects to handle leave messages
    """
    connection = DryRunConnection()
    joinMessage = """>testroom
|J|#Ann(ik)a ^_^"""

    core.Message(joinMessage, connection)
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))
    message = core.Message(
        """>testroom
|L|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "leave"
    assert 'testroom' not in connection.getUserRooms(connection.getUser('annika'))

    core.Message(joinMessage, connection)
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))
    message = core.Message(
        """>testroom
|l|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "leave"
    assert 'testroom' not in connection.getUserRooms(connection.getUser('annika'))

    core.Message(joinMessage, connection)
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))
    message = core.Message(
        """>testroom
|leave|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "leave"
    assert 'testroom' not in connection.getUserRooms(connection.getUser('annika'))

def testMessagePM():
    """Tests the ability of Message objects to handle PM messages and commands
    """
    message = core.Message(
        "|pm|+aNNika ^_^|Expecto Botronum|~somecommand argument1,argumENT2||withpipes, argumént3",
        DryRunConnection()
    )
    assert message.senderName == "+aNNika ^_^"
    assert message.sender.id == "annika"
    assert message.arguments == ["~somecommand", "argument1", "argumENT2||withpipes", " argumént3"]
    assert message.room is None
    assert message.body == "~somecommand argument1,argumENT2||withpipes, argumént3"
    assert message.time is None
    assert message.type == 'pm'
    assert message.challstr is None

def testMessageQueryResponse():
    """Tests the ability of Message objects to handle query responses
    """
    connection = DryRunConnection()
    message = core.Message(
        """|queryresponse|roominfo|{"id":"testroom","roomid":"testroom","title":"Magic & Mayhem","type":"chat","visibility":"hidden","modchat":null,"auth":{"#":["annika","awa","cleo","meicoo"],"%":["dawnofares","instruct","ratisweep","pirateprincess","watfor","oaklynnthylacine"],"@":["gwynt","darth","profsapling","ravioliqueen","miapi"],"+":["madmonty","birdy","captanpasta","iwouldprefernotto","xprienzo","nui","toxtricityamped"],"*":["expectobotronum","kida"]}, "users":["user1","user2"]}""",
        connection
    )
    assert message.type == "queryresponse"
    assert "testroom" in connection.userList[connection.getUser('user1')]
    assert "testroom" in connection.userList[connection.getUser('user2')]

    allUserIDs = [user.id for user in connection.userList.keys()]
    assert 'user1' in allUserIDs
    assert 'user2' in allUserIDs

    auth = connection.getRoomByID("testroom").auth
    assert auth['#'] == {"annika", "awa", "cleo", "meicoo"}
    assert auth['*'] == {"expectobotronum", "kida"}
    assert auth['@'] == {"gwynt", "darth", "profsapling", "ravioliqueen", "miapi"}
    assert auth['%'] == {"dawnofares", "instruct", "ratisweep", "pirateprincess", "watfor", "oaklynnthylacine"}
    assert auth['+'] == {"madmonty", "birdy", "captanpasta", "iwouldprefernotto", "xprienzo", "nui", "toxtricityamped"}

## Room Object Tests ##
def testRoomAuth():
    """Tests the ability of Room objects to handle updating and checking auth
    """
    connection = DryRunConnection()
    room = core.Room("testroom", connection)

    assert room.auth == {}
    room.updateAuth({'#': {'owner1', 'owner2'}, '*': {'bot1', 'bot2'}, '@': {'mod1', 'mod2'}})
    assert room.auth == {'#': {'owner1', 'owner2'}, '*': {'bot1', 'bot2'}, '@': {'mod1', 'mod2'}}
    room.updateAuth({'%': {'driver1', 'driver2'}, '+': {'voice1', 'voice2'}})
    assert room.auth == {'#': {'owner1', 'owner2'}, '*': {'bot1', 'bot2'}, '@': {'mod1', 'mod2'}, '%': {'driver1', 'driver2'}, '+': {'voice1', 'voice2'}}

    assert room.usersWithRankGEQ('#') == {'owner1', 'owner2'}
    assert room.usersWithRankGEQ('*') == {'owner1', 'owner2', 'bot1', 'bot2'}
    assert room.usersWithRankGEQ('@') == {'owner1', 'owner2', 'bot1', 'bot2', 'mod1', 'mod2'}
    assert room.usersWithRankGEQ('%') == {'owner1', 'owner2', 'bot1', 'bot2', 'mod1', 'mod2', 'driver1', 'driver2'}
    assert room.usersWithRankGEQ('+') == {'owner1', 'owner2', 'bot1', 'bot2', 'mod1', 'mod2', 'driver1', 'driver2', 'voice1', 'voice2'}

    assert isinstance(str(room), str)

def testRoomJoinphrases():
    """Tests the joinphrase storage of Room objects
    """
    room = core.Room("testroom", DryRunConnection())

    assert room.joinphrases == {}
    room.addJoinphrase("jp1éé || ~uwu~", "user1")
    assert room.joinphrases == {'user1': "jp1éé || ~uwu~"}
    room.removeJoinphrase("user1")
    assert room.joinphrases == {}

## User Object Tests ##
def testUser():
    """Tests the User object
    """
    connection = DryRunConnection()
    user = core.User("&tEsT uSeR ~o///o~", connection)
    room = core.Room("testroom", connection)

    assert user.name == "&tEsT uSeR ~o///o~"
    assert user.id == "testuseroo"
    assert not user.isAdmin

    room.auth = {}
    assert not user.can("html", room)
    assert not user.can("wall", room)
    assert not user.can("admin", room)

    room.auth = {'%': {'testuseroo'}}
    assert not user.can("html", room)
    assert user.can("wall", room)
    assert not user.can("admin", room)

    room.auth = {'*': {'testuseroo'}}
    assert user.can("html", room)
    assert user.can("wall", room)
    assert not user.can("admin", room)

    user.isAdmin = True
    room.auth = {}
    assert user.can("html", room)
    assert user.can("wall", room)
    assert user.can("admin", room)
    assert user.can("manage", room)

    assert isinstance(str(user), str)

## Connection Object Tests
## TODO: write these
def testConnection():
    """tests the Connection object
    """
    connection = DryRunConnection()

    assert connection.commands

    connection.userJoinedRoom(core.User("user1", connection), connection.getRoomByName("tE ST r]OOm"))
    assert connection.userList[connection.getUser("user1")] == {"testroom"}
    assert connection.getUserRooms(connection.getUser("user1")) == {"testroom"}

    connection.userLeftRoom(connection.getUser("user1"), connection.getRoomByID("testroom"))
    assert connection.userList[connection.getUser("user1")] == set()
    assert connection.getUserRooms(connection.getUser("user1")) == set()

    assert connection.getRoomByID("testroom").id == "testroom"
    assert connection.getRoomByName("T e s tROO  &%# m").id == "testroom"

    assert isinstance(str(connection), str)