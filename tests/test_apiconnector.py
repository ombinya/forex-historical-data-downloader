import unittest
from deriv_api import DerivAPI
from ..apiconnector import APIConnector


class TestAPIConnector(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
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

if __name__ == "__main__":
    unittest.main()