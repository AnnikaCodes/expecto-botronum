"""test_core.py
    tests for core
    by Annika"""

# pylint: disable=line-too-long
from typing import Any
import pytest # type: ignore

import psclient # type: ignore
import core
import config
from dummies import DummyConnection, DummyUser

def testToID() -> None:
    """Tests the toID() function
    """
    assert psclient.toID("hi") == "hi"
    assert psclient.toID("HI") == "hi"
    assert psclient.toID("$&@*%$HI   ^4åå") == "hi4"

def testLog(capsys: Any) -> None:
    """Tests the log() function
    """
    config.loglevel = 0
    core.log("E: this shows")
    core.log("W: this doesn't show")
    core.log("I: this doesn't show")
    core.log("DEBUG: this doesn't show")
    core.log("this doesn't show")
    capture = capsys.readouterr()
    assert capture.out == ""
    assert capture.err == "E: this shows\n"

    config.loglevel = 1
    core.log("E: this shows")
    core.log("W: this shows")
    core.log("I: this doesn't show")
    core.log("DEBUG: this doesn't show")
    core.log("this doesn't show")
    capture = capsys.readouterr()
    assert capture.out == ""
    assert capture.err == "E: this shows\nW: this shows\n"

    config.loglevel = 2
    core.log("E: this shows")
    core.log("W: this shows")
    core.log("I: this shows")
    core.log("DEBUG: this doesn't show")
    core.log("this doesn't show")
    capture = capsys.readouterr()
    assert capture.out == "I: this shows\n"
    assert capture.err == "E: this shows\nW: this shows\n"

    config.loglevel = 3
    core.log("E: this shows")
    core.log("W: this shows")
    core.log("I: this shows")
    core.log("DEBUG: this shows")
    core.log("this shows")
    capture = capsys.readouterr()
    assert capture.out == "I: this shows\nDEBUG: this shows\nthis shows\n"
    assert capture.err == "E: this shows\nW: this shows\n"

## Tests for Message objects ##
def testMessageChallstr() -> None:
    """Tests the ability of Message objects to handle challstrs
    """
    message = core.BotMessage(
        "|challstr|4|314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823",
        DummyConnection()
    )
    assert message.challstr == "4|314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823"

def testMessageChat() -> None:
    """Tests the ability of Message objects to parse chat messages including strange characters, from the Lobby
    """
    message = core.BotMessage(
        "|c|#Ann/ika ^_^|Hi, I wrote a Python test|Isn't it cool?it,contains,odd characters och konstigt bokstaver från andra språk.",
        DummyConnection()
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

def testMessageChatCommand() -> None:
    """Tests the ability of Message objects to handle commands sent to rooms, with arguments
    """
    message = core.BotMessage(
        """>testroom
|c:|1593475694|#Ann/ika ^_^|-somecommand argument1,argumENT2||withpipes, argumént3""",
        DummyConnection()
    )
    assert message.senderName == "#Ann/ika ^_^"
    assert message.sender.id == "annika"
    assert message.arguments == ["-somecommand", "argument1", "argumENT2||withpipes", " argumént3"]
    assert message.room.id == "testroom"
    assert message.body == "-somecommand argument1,argumENT2||withpipes, argumént3"
    assert message.time == "1593475694"
    assert message.type == 'chat'
    assert message.challstr is None


def testMessageJoin() -> None:
    """Tests the ability of Message objects to handle join messages
    """
    connection = DummyConnection()
    message = core.BotMessage(
        """>testroom
|J|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "join"
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))

    message = core.BotMessage(
        """>testroom2
|j|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "join"
    assert 'testroom2' in connection.getUserRooms(connection.getUser('annika'))

    message = core.BotMessage(
        """>testroom3
|join|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "join"
    assert 'testroom3' in connection.getUserRooms(connection.getUser('annika'))

def testMessageLeave() -> None:
    """Tests the ability of Message objects to handle leave messages
    """
    connection = DummyConnection()
    joinMessage = """>testroom
|J|#Ann(ik)a ^_^"""

    core.BotMessage(joinMessage, connection)
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))
    message = core.BotMessage(
        """>testroom
|L|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "leave"
    assert 'testroom' not in connection.getUserRooms(connection.getUser('annika'))

    core.BotMessage(joinMessage, connection)
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))
    message = core.BotMessage(
        """>testroom
|l|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "leave"
    assert 'testroom' not in connection.getUserRooms(connection.getUser('annika'))

    core.BotMessage(joinMessage, connection)
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))
    message = core.BotMessage(
        """>testroom
|leave|#Ann(ik)a ^_^""",
        connection
    )
    assert message.type == "leave"
    assert 'testroom' not in connection.getUserRooms(connection.getUser('annika'))

def testMessagePM() -> None:
    """Tests the ability of Message objects to handle PM messages and commands
    """
    message = core.BotMessage(
        "|pm|+aNNika ^_^|Expecto Botronum|-somecommand argument1,argumENT2||withpipes, argumént3",
        DummyConnection()
    )
    assert message.senderName == "+aNNika ^_^"
    assert message.sender.id == "annika"
    assert message.arguments == ["-somecommand", "argument1", "argumENT2||withpipes", " argumént3"]
    assert message.room is None
    assert message.body == "-somecommand argument1,argumENT2||withpipes, argumént3"
    assert message.time is None
    assert message.type == 'pm'
    assert message.challstr is None

def testMessageQueryResponse() -> None:
    """Tests the ability of Message objects to handle query responses
    """
    connection = DummyConnection()
    message = core.BotMessage(
        """|queryresponse|roominfo|{"id":"testroom","roomid":"testroom","title":"Magic & Mayhem","type":"chat","visibility":"hidden","modchat":null,"auth":{"#":["annika","awa","cleo","meicoo"],"%":["dawnofares","instruct","ratisweep","pirateprincess","watfor","oaklynnthylacine"],"@":["gwynt","darth","profsapling","ravioliqueen","miapi"],"+":["madmonty","birdy","captanpasta","iwouldprefernotto","xprienzo","nui","toxtricityamped"],"*":["expectobotronum","kida"]}, "users":["user1","user2"]}""",
        connection
    )
    assert message.type == "queryresponse"
    assert "testroom" in connection.userList[connection.getUser('user1')]
    assert "testroom" in connection.userList[connection.getUser('user2')]

    allUserIDs = [user.id for user in connection.userList.keys()]
    assert 'user1' in allUserIDs
    assert 'user2' in allUserIDs

    auth = connection.getRoom("testroom").auth
    assert auth['#'] == {"annika", "awa", "cleo", "meicoo"}
    assert auth['*'] == {"expectobotronum", "kida"}
    assert auth['@'] == {"gwynt", "darth", "profsapling", "ravioliqueen", "miapi"}
    assert auth['%'] == {"dawnofares", "instruct", "ratisweep", "pirateprincess", "watfor", "oaklynnthylacine"}
    assert auth['+'] == {"madmonty", "birdy", "captanpasta", "iwouldprefernotto", "xprienzo", "nui", "toxtricityamped"}

## Room Object Tests ##
class TestRoom:
    """Tests for Room objects
    """
    connection = DummyConnection()
    room = core.BotRoom("testroom", connection)

    def testRoomAuth(self) -> None:
        """Tests the ability of Room objects to handle updating and checking auth
        """
        assert self.room.auth == {}
        self.room.updateAuth({'#': {'owner1', 'owner2'}, '*': {'bot1', 'bot2'}, '@': {'mod1', 'mod2'}})
        assert self.room.auth == {'#': {'owner1', 'owner2'}, '*': {'bot1', 'bot2'}, '@': {'mod1', 'mod2'}}
        self.room.updateAuth({'%': {'driver1', 'driver2'}, '+': {'voice1', 'voice2'}})
        assert self.room.auth == {'#': {'owner1', 'owner2'}, '*': {'bot1', 'bot2'}, '@': {'mod1', 'mod2'}, '%': {'driver1', 'driver2'}, '+': {'voice1', 'voice2'}}

        assert self.room.usersWithRankGEQ('#') == {'owner1', 'owner2'}
        assert self.room.usersWithRankGEQ('*') == {'owner1', 'owner2', 'bot1', 'bot2'}
        assert self.room.usersWithRankGEQ('@') == {'owner1', 'owner2', 'bot1', 'bot2', 'mod1', 'mod2'}
        assert self.room.usersWithRankGEQ('%') == {'owner1', 'owner2', 'bot1', 'bot2', 'mod1', 'mod2', 'driver1', 'driver2'}
        assert self.room.usersWithRankGEQ('+') == {'owner1', 'owner2', 'bot1', 'bot2', 'mod1', 'mod2', 'driver1', 'driver2', 'voice1', 'voice2'}

        assert isinstance(str(self.room), str)

    def testRoomJoinphrases(self) -> None:
        """Tests the joinphrase storage of Room objects
        """
        assert self.room.joinphrases == {}
        self.room.addJoinphrase("jp1éé || ~uwu~", "user1")
        assert self.room.joinphrases == {'user1': "jp1éé || ~uwu~"}
        self.room.removeJoinphrase("user1")
        assert self.room.joinphrases == {}

## User Object Tests ##
def testUser() -> None:
    """Tests the User object
    """
    connection = DummyConnection()
    user = DummyUser("&tEsT uSeR ~o///o~", connection)
    room = core.BotRoom("testroom", connection)

    assert user.name == "&tEsT uSeR ~o///o~"
    assert user.id == "testuseroo"
    assert user.id not in config.sysops

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

    assert isinstance(str(user), str)

## Connection Object Tests
def testConnection() -> None:
    """tests the Connection object
    """
    connection = DummyConnection()

    assert connection.commands

    connection.userJoinedRoom(core.BotUser("user1", connection), connection.getRoom("tE ST r]OOm"))
    assert connection.userList[connection.getUser("user1")] == {"testroom"}
    assert connection.getUserRooms(connection.getUser("user1")) == {"testroom"}

    connection.userLeftRoom(connection.getUser("user1"), connection.getRoom("testroom"))
    assert connection.userList[connection.getUser("user1")] == set()
    assert connection.getUserRooms(connection.getUser("user1")) == set()

    assert connection.getRoom("testroom").id == "testroom"
    assert connection.getRoom("T e s tROO  &%# m").id == "testroom"

    assert isinstance(str(connection), str)
