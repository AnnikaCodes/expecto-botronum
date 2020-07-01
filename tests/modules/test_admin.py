"""test_admin.py
    tests for admin
    by Annika"""

import dummies
import admin

class TestAdmin():
    """Test the admin module
    """
    module = admin.Module()
    def testEval(self):
        """Tests the eval command
        """
        message = dummies.DummyMessage(
            arguments=["~eval", "(2 + 2**2) / 2"],
            sender=dummies.DummyUser(isAdmin=True, userid='annika')
        )
        self.module.eval(message)
        assert message.response.strip("!code ").strip('\n').strip('`') == f"{(2 + 2**2) / 2}"

    def testModuleHandling(self):
        """Tests the module loading/unloading methods (not commands)
        """
        connection = dummies.DummyConnection()
        assert "base" in connection.modules
        assert "ping" in connection.commands.keys()

        self.module.unload(connection, "base")
        assert "base" not in connection.modules
        assert "ping" not in connection.commands.keys()

        self.module.load(connection, "base")
        assert "base" in connection.modules
        assert "ping" in connection.commands.keys()

    # The other commands in admin aren't really objectively testable
