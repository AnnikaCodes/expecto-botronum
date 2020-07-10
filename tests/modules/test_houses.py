"""test_houses.py

    tests for houses

    by Annika"""

import houses

# Houses is completely dependent on `data.json`, so testing is impossible

class TestHouses():
    """Test the houses module
    """
    module = houses.Module()

    def testHousesExist(self):
        """Tests the snippet-counting command
        """
        assert len(self.module.commands) > 3
