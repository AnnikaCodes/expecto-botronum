"""test_superhero.py
    tests for superhero
    by Annika"""

import pytest

import dummies
import superhero
import config

class TestSuperhero():
    """Test the superhero module
    """
    module = superhero.Module()

    @pytest.mark.xfail(reason="will fail due to a known bug described in issue #32")
    def testInitializeData(self):
        # pylint: disable=protected-access
        """Tests initializing data for the Superhero API
        """
        data = superhero._initializeData()
        assert len(data.keys()) == data[list(data.keys())[-1]]

    @pytest.mark.skipif(len(config.superheroAPIKey) < 1, reason="no Superhero API key found")
    def testSuperhero(self):
        """Tests the superhero command
        """
        # This might have issues since it relies on the API responses not changing, but there's not a great way to test this.
        message = dummies.DummyMessage(arguments=["~superhero", "t H\\ orå"])
        self.module.superhero(message)
        assert not message.response
        assert "Thor" in message.HTMLResponse
        assert "Loki (step-brother)" in message.HTMLResponse
        assert "Asgardian" in message.HTMLResponse
        assert "King of Asgard" in message.HTMLResponse
