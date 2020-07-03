"""test_games.py
    tests for games
    by Annika"""

import dummies
import games

class TestGames():
    """Test the games module
    """
    module = games.Module()
    connection = dummies.DummyConnection()

    def testReversio(self):
        """Tests the reversio commands
        """
        self.module.reversioWords = {"testroom": []}
        assert self.module.reversioWords["testroom"] == []

        message = dummies.DummyMessage(
            arguments=["~addreversioword", "testroom", "Test Word"],
            sender=dummies.DummyUser(isAdmin=True)
        )
        self.module.addReversioWord(message)
        assert len(self.module.reversioWords["testroom"]) == 1
        assert self.module.reversioWords["testroom"][0].lower().strip() == "test word"

        message = dummies.DummyMessage(arguments=["~reverse", "testroom"])
        self.module.reverse(message)
        assert message.response == "/wall drow tset"

        message = dummies.DummyMessage(
            arguments=["~rmreversioword", "testroom", "Test Word"],
            sender=dummies.DummyUser(isAdmin=True)
        )
        self.module.removeReversioWord(message)
        assert len(self.module.reversioWords["testroom"]) == 0

    def testMinigameLB(self):
        """Tests the minigame leaderboard functionality
        """
        assert len(self.module.minigamePoints.keys()) == 0

        message = dummies.DummyMessage(
            arguments=["~addpoints", "testuser"],
            sender=dummies.DummyUser(isAdmin=True),
            room=self.connection.getRoom("testroom")
        )
        self.module.addPoints(message)
        assert self.module.minigamePoints["testroom"]["testuser"] == 1

        message = dummies.DummyMessage(
            arguments=["~addpoints", "testuser", "-2"],
            sender=dummies.DummyUser(isAdmin=True),
            room=self.connection.getRoom("testroom")
        )
        self.module.addPoints(message)
        assert self.module.minigamePoints["testroom"]["testuser"] == -1

    def testIsInt(self):
        """Tests the isInt() helper function provided by the games module
        """
        assert not games.isInt("a")
        assert not games.isInt("5925a93")
        assert not games.isInt("å425")
        assert not games.isInt("z424")
        assert not games.isInt("24.0")
        assert not games.isInt("3.14159")
        assert games.isInt("2")
        assert games.isInt("4924")
        assert games.isInt("-1")
        assert games.isInt("-0")
        assert games.isInt("001230")
        assert games.isInt(str(2**1000))
