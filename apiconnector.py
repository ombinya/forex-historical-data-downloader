import websockets
from deriv_api import DerivAPI
from dotenv import load_dotenv
import os
import asyncio
import socket

class APIConnector:
    def __init__(self):
        load_dotenv()
        self.derivappid = os.environ.get("DERIV_APP_ID")
        self.apiconnection = None

    async def create_api_connection(self):
        """
        Creates a connection to the DERIV API.
        """

        connection = await websockets.connect(
            'wss://ws.derivws.com/websockets/v3?app_id={}'.format(self.derivappid)
        )

        self.apiconnection = DerivAPI(connection=connection)

    # async def get_asset_index(self, apiconnection):
    #     assets = await apiconnection.asset_index({"asset_index": 1})
    #     return assets

    async def ticks_history(self, startepoch, duration, asset):
        """
        Retrieves historical tick data for a given asset, from the start epoch to the end epoch.

        :param startepoch: the start epoch
        :return: dictionary object containing the retrieved forex data
        """

        endepoch = startepoch + duration - 1
        tickshistory = await self.apiconnection.ticks_history(
            {
                "ticks_history": asset,
                "end": endepoch,
                "start": startepoch
            }
        )

        return tickshistory


if __name__ == "__main__":
    async def main():
        apiConnector = APIConnector()
        try:
            apiConnector.apiconnection = await apiConnector.create_api_connection()
        except socket.gaierror:
            pass

        startEpoch = 1722816000
        # endEpoch = startEpoch + 7200
        duration = 3600
        ticksHistory = await apiConnector.ticks_history(startEpoch, duration, "frxAUDJPY")
        assert int(ticksHistory["echo_req"]["end"]) <= startEpoch + duration
        print(ticksHistory)

    asyncio.run(main())


