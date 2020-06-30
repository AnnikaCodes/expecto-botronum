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
    testMsg = core.Message(
        "|challstr|4|314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823",
        DryRunConnection()
    )
    assert testMsg.challstr == "4|314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823"

def testMessageChat():
    """Tests the ability of Message objects to parse chat messages including strange characters, from the Lobby
    """
    testMsg = core.Message(
        "|c|#Ann/ika ^_^|Hi, I wrote a Python test|Isn't it cool?it,contains,odd characters och konstigt bokstaver från andra språk.",
        DryRunConnection()
    )
    assert testMsg.senderName == "#Ann/ika ^_^"
    assert testMsg.sender.id == "annika"
    assert testMsg.arguments == ['Hi,', "I wrote a Python test|Isn't it cool?it", "contains", "odd characters och konstigt bokstaver från andra språk."]
    assert testMsg.room.id == "lobby"
    assert testMsg.body == "Hi, I wrote a Python test|Isn't it cool?it,contains,odd characters och konstigt bokstaver från andra språk."
    assert testMsg.time is None
    assert testMsg.type == 'chat'
    assert testMsg.challstr is None

def testMessageChatCommand():
    """Tests the ability of Message objects to handle commands sent to rooms, with arguments
    """
    testMsg = core.Message(
        """>testroom
|c:|1593475694|#Ann/ika ^_^|~somecommand argument1,argumENT2||withpipes, argumént3""",
        DryRunConnection()
    )
    assert testMsg.senderName == "#Ann/ika ^_^"
    assert testMsg.sender.id == "annika"
    assert testMsg.arguments == ["~somecommand", "argument1", "argumENT2||withpipes", " argumént3"]
    assert testMsg.room.id == "testroom"
    assert testMsg.body == "~somecommand argument1,argumENT2||withpipes, argumént3"
    assert testMsg.time == "1593475694"
    assert testMsg.type == 'chat'
    assert testMsg.challstr is None


def testMessageJoin():
    """Tests the ability of Message objects to handle join messages
    """
    connection = DryRunConnection()
    testMsg = core.Message(
        """>testroom
|J|#Ann(ik)a ^_^""",
        connection
    )
    assert testMsg.type == "join"
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))

    testMsg = core.Message(
        """>testroom2
|j|#Ann(ik)a ^_^""",
        connection
    )
    assert testMsg.type == "join"
    assert 'testroom2' in connection.getUserRooms(connection.getUser('annika'))

    testMsg = core.Message(
        """>testroom3
|join|#Ann(ik)a ^_^""",
        connection
    )
    assert testMsg.type == "join"
    assert 'testroom3' in connection.getUserRooms(connection.getUser('annika'))

def testMessageLeave():
    """Tests the ability of Message objects to handle leave messages
    """
    connection = DryRunConnection()
    joinMessage = """>testroom
|J|#Ann(ik)a ^_^"""

    core.Message(joinMessage, connection)
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))
    testMsg = core.Message(
        """>testroom
|L|#Ann(ik)a ^_^""",
        connection
    )
    assert testMsg.type == "leave"
    assert 'testroom' not in connection.getUserRooms(connection.getUser('annika'))

    core.Message(joinMessage, connection)
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))
    testMsg = core.Message(
        """>testroom
|l|#Ann(ik)a ^_^""",
        connection
    )
    assert testMsg.type == "leave"
    assert 'testroom' not in connection.getUserRooms(connection.getUser('annika'))

    core.Message(joinMessage, connection)
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))
    testMsg = core.Message(
        """>testroom
|leave|#Ann(ik)a ^_^""",
        connection
    )
    assert testMsg.type == "leave"
    assert 'testroom' not in connection.getUserRooms(connection.getUser('annika'))

def testMessagePM():
    """Tests the ability of Message objects to handle PM messages and commands
    """
    testMsg = core.Message(
        "|pm|+aNNika ^_^|Expecto Botronum|~somecommand argument1,argumENT2||withpipes, argumént3",
        DryRunConnection()
    )
    assert testMsg.senderName == "+aNNika ^_^"
    assert testMsg.sender.id == "annika"
    assert testMsg.arguments == ["~somecommand", "argument1", "argumENT2||withpipes", " argumént3"]
    assert testMsg.room is None
    assert testMsg.body == "~somecommand argument1,argumENT2||withpipes, argumént3"
    assert testMsg.time is None
    assert testMsg.type == 'pm'
    assert testMsg.challstr is None

def testMessageQueryResponse():
    """Tests the ability of Message objects to handle query responses
    """
    connection = DryRunConnection()
    testMsg = core.Message(
        """|queryresponse|roominfo|{"id":"testroom","roomid":"testroom","title":"Magic & Mayhem","type":"chat","visibility":"hidden","modchat":null,"auth":{"#":["annika","awa","cleo","meicoo"],"%":["dawnofares","instruct","ratisweep","pirateprincess","watfor","oaklynnthylacine"],"@":["gwynt","darth","profsapling","ravioliqueen","miapi"],"+":["madmonty","birdy","captanpasta","iwouldprefernotto","xprienzo","nui","toxtricityamped"],"*":["expectobotronum","kida"]}, "users":["user1","user2"]}""",
        connection
    )
    assert testMsg.type == "queryresponse"
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

## Connection Object Tests
## TODO: write these
