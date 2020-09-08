"""test_joinphrase.py
    tests for joinphrase
    by Annika"""

import dummies
import joinphrase

class TestJoinphrase():
    """Test the joinphrase module
    """
    module = joinphrase.Module()
    connection = dummies.DummyConnection()

    def testJoinphrase(self) -> None:
        """Tests adding and removing joinphrases through commands
        """
        # Remove any previous `testroom2` data left in data.json
        for user in list(self.connection.getRoom("testroom2").joinphrases.keys()):
            self.connection.getRoom("testroom2").removeJoinphrase(user)

        assert len(self.connection.getRoom("testroom2").joinphrases) == 0
        message = dummies.DummyMessage(
            arguments=["-addjp", "testroom2", "Test User", "Join pHRase &&||"],
            sender=dummies.DummyUser(isAdmin=True),
            connection=self.connection
        ) # Adding in PMs
        self.module.addJP(message)
        assert len(self.connection.getRoom("testroom2").joinphrases) == 1
        assert self.connection.getRoom("testroom2").joinphrases["testuser"] == "Join pHRase &&||"

        message = dummies.DummyMessage(
            arguments=["-removejp", "testroom2", "Test User"],
            sender=dummies.DummyUser(isAdmin=True),
            connection=self.connection
        ) # Removing in PMs
        self.module.deleteJP(message)
        assert len(self.connection.getRoom("testroom2").joinphrases) == 0

        message = dummies.DummyMessage(
            arguments=["-addjp", "Test User", "Join pHRase &&||"],
            sender=dummies.DummyUser(isAdmin=True),
            room=self.connection.getRoom("testroom2")
        ) # Adding in a room
        self.module.addJP(message)
        assert len(self.connection.getRoom("testroom2").joinphrases) == 1
        assert self.connection.getRoom("testroom2").joinphrases["testuser"] == "Join pHRase &&||"

        message = dummies.DummyMessage(
            arguments=["-removejp", "Test User"],
            sender=dummies.DummyUser(isAdmin=True),
            room=self.connection.getRoom("testroom2")
        ) # Removing in a room
        self.module.deleteJP(message)
        assert len(self.connection.getRoom("testroom2").joinphrases) == 0
