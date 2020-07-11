"""test_base.py
    tests for base
    by Annika"""

from dummies import DummyMessage
import base

class TestBase():
    """Test the base module
    """
    module = base.Module()

    def testPing(self) -> None:
        """Tests the ping command
        """
        message = DummyMessage()
        self.module.ping(message)
        assert message.response == "Pong!"

    def testOwo(self) -> None:
        """Tests the owo command
        """
        message = DummyMessage(arguments=["~owo", "I Am a TEST for", " the OWO command."])
        self.module.owo(message)
        assert message.response == "IwI AwAm awa TEwEST fowor, thewe OwOWOwO cowommawand."

    def testUwu(self) -> None:
        """Tests the uwu command
        """
        # Test message courtesy of Mia
        passResponse = "What kind of Wynywd Skynywd, Confedewate fwag fwying outside of evewy twaiwew, "
        passResponse += "Chevy symbow chest tattoo, MAGA hat weawing, six yeaw owd son stiww in diapews, "
        passResponse += "wife is wike a box of chocowates, sweet tea bwewing, moon shine wunning, mountain dew dwinking, "
        passResponse += "NASCAW woving, piwe of empty but wight cans in the passengew seat of the beat down pickup shit is this?"
        message = DummyMessage(arguments=[
            "~uwu", "What kind of Lynyrd Skynyrd", " Confederate flag flying outside of every trailer",
            " Chevy symbol chest tattoo", " MAGA hat wearing", " six year old son still in diapers",
            " life is like a box of chocolates", " sweet tea brewing", " moon shine running", " mountain dew drinking",
            " NASCAR loving", " pile of empty but light cans in the passenger seat of the beat down pickup shit is this?"
        ])

        self.module.uwu(message)
        assert message.response == passResponse

    def testTimer(self) -> None:
        """Tests the timer command
        """
        message = DummyMessage(arguments=['~timer', "0.01", "message"])
        self.module.timer(message)
        assert not message.response
