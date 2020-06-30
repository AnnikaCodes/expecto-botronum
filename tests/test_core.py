#### test_core.py #####
## Tests for core    ##
## Written by Annika ##
#######################

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).joinpath("../..").resolve()) + '/')
import core

## Helper Classes ##
class DryRunConnection(core.Connection):
    def __init__(self):
        super().__init__()
        self.roomList = {core.Room("testroom", self), core.Room("lobby", self)}

    def send(self, message):
        pass

## Tests for Message objects ##
def testMessageChallstr():
    testMsg = core.Message(
        "|challstr|4|314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823",
        DryRunConnection()
    )
    assert testMsg.challstr == "4|314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823"

def testMessageChat():
    testMsg = core.Message(
        "|c|#Ann/ika ^_^|Hi, I wrote a Python test|Isn't it cool?it,contains,odd characters och konstigt bokstaver från andra språk.",
        DryRunConnection()
    )
    assert testMsg.senderName == "#Ann/ika ^_^"
    assert testMsg.sender.id == "annika"
    assert testMsg.arguments == ['Hi,', "I wrote a Python test|Isn't it cool?it", "contains", "odd characters och konstigt bokstaver från andra språk."]
    assert testMsg.room.id == "lobby"
    assert testMsg.body == "Hi, I wrote a Python test|Isn't it cool?it,contains,odd characters och konstigt bokstaver från andra språk."
    assert testMsg.time == None
    assert testMsg.type == 'chat'
    assert testMsg.challstr == None

def testMessageChatCommand():
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
    assert testMsg.challstr == None


def testMessageJoin():
    connection = DryRunConnection()
    testMsg = core.Message(
        """>testroom
|J|#Ann(ik)a ^_^""",
        connection
    )
    assert testMsg.type == "join"
    assert 'testroom' in connection.getUserRooms(connection.getUser('annika'))

def testMessageLeave():
    connection = DryRunConnection()

    # Set up
    core.Message(
        """>testroom
|J|#Ann(ik)a ^_^""",
        connection
    )

    testMsg = core.Message(
        """>testroom
|L|#Ann(ik)a ^_^""",
        connection
    )
    assert testMsg.type == "leave"
    assert 'testroom' not in connection.getUserRooms(connection.getUser('annika'))

def testMessagePM():
    testMsg = core.Message(
        "|pm|+aNNika ^_^|Expecto Botronum|~somecommand argument1,argumENT2||withpipes, argumént3",
        DryRunConnection()
    )
    assert testMsg.senderName == "+aNNika ^_^"
    assert testMsg.sender.id == "annika"
    assert testMsg.arguments == ["~somecommand", "argument1", "argumENT2||withpipes", " argumént3"]
    assert testMsg.room == None
    assert testMsg.body == "~somecommand argument1,argumENT2||withpipes, argumént3"
    assert testMsg.time == None
    assert testMsg.type == 'pm'
    assert testMsg.challstr == None

def testMessageQueryResponse():
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
    connection = DryRunConnection()
    room = core.Room("testroom", connection)

    assert room.auth == {}
    room.updateAuth({'#': {'owner1', 'owner2'}, '*': {'bot1', 'bot2'},'@': {'mod1', 'mod2'}})
    assert room.auth == {'#': {'owner1', 'owner2'}, '*': {'bot1', 'bot2'},'@': {'mod1', 'mod2'}}
    room.updateAuth({'%': {'driver1', 'driver2'}, '+': {'voice1', 'voice2'}})
    assert room.auth == {'#': {'owner1', 'owner2'}, '*': {'bot1', 'bot2'},'@': {'mod1', 'mod2'}, '%': {'driver1', 'driver2'}, '+': {'voice1', 'voice2'}}

    assert room.usersWithRankGEQ('#') == {'owner1', 'owner2'}
    assert room.usersWithRankGEQ('*') == {'owner1', 'owner2', 'bot1', 'bot2'}
    assert room.usersWithRankGEQ('@') == {'owner1', 'owner2', 'bot1', 'bot2', 'mod1', 'mod2'}
    assert room.usersWithRankGEQ('%') == {'owner1', 'owner2', 'bot1', 'bot2', 'mod1', 'mod2', 'driver1', 'driver2'}
    assert room.usersWithRankGEQ('+') == {'owner1', 'owner2', 'bot1', 'bot2', 'mod1', 'mod2', 'driver1', 'driver2', 'voice1', 'voice2'}

def testRoomJoinphrases():
    connection = DryRunConnection()
    room = core.Room("testroom", connection)

    assert room.joinphrases == {}
    room.addJoinphrase("jp1éé || ~uwu~", "user1")
    assert room.joinphrases == {'user1': "jp1éé || ~uwu~"}
    room.removeJoinphrase("user1")
    assert room.joinphrases == {}


