import unittest
from deriv_api import DerivAPI
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.apiconnector import APIConnector


class TestAPIConnector(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.apiconnector = APIConnector()

    async def test_create_api_connection(self):
        await self.apiconnector.create_api_connection()
        self.assertIsInstance(self.apiconnector.apiconnection, DerivAPI)

    async def test_ticks_history(self):
        startEpoch = 1722816000
        duration = 3600

        await self.apiconnector.create_api_connection()
        ticksHistory = await self.apiconnector.ticks_history(startEpoch, duration, "frxAUDJPY")
        self.assertLessEqual(int(ticksHistory["echo_req"]["end"]), startEpoch + duration)
        self.assertGreaterEqual(int(ticksHistory["echo_req"]["start"]), startEpoch)

if __name__ == "__main__":
    unittest.main()