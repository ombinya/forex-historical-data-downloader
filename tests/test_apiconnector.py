import unittest
from deriv_api import DerivAPI
from ..apiconnector import APIConnector


class TestAPIConnector(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.apiconnector = APIConnector()

    async def test_create_api_connection(self):
        apiconnection = await self.apiconnector.create_api_connection()
        self.assertIsInstance(apiconnection, DerivAPI)


if __name__ == "__main__":
    unittest.main()