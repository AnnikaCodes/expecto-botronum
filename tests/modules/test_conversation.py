"""test_conversation.py
    tests for conversation
    by Annika"""

import dummies
import conversation

# Conversation is difficult to test, since its desired output is mostly very reliant on `data.json`

class TestConversation():
    """Test the conversation module
    """
    module = conversation.Module()

    def testCountSnippets(self) -> None:
        """Tests the snippet-counting command
        """
        message = dummies.DummyMessage(arguments=["~countfacts", "testroom"])
        self.module.countSnippets(message)
        assert message.response and "0" in message.response

        message = dummies.DummyMessage(arguments=["~counttopics", "testroom"])
        self.module.countSnippets(message)
        assert message.response and "0" in message.response

        message = dummies.DummyMessage(arguments=["~countquotes", "testroom"])
        self.module.countSnippets(message)
        assert message.response and "0" in message.response
