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

    async def create_api_connection(self):
        """
        Creates a connection to the DERIV API.
        """

        connection = await websockets.connect(
            'wss://ws.derivws.com/websockets/v3?app_id={}'.format(self.derivappid)
        )

        apiconnection = DerivAPI(connection=connection)

        return apiconnection

    async def get_asset_index(self, apiconnection):
        assets = await apiconnection.asset_index({"asset_index": 1})
        return assets

    async def ticks_history(self, startepoch, duration, asset, apiconnection):
        """
        Retrieves historical tick data for a given asset, from the start epoch to the end epoch.

        :param startepoch: the start epoch
        :return: dictionary object containing the retrieved forex data
        """

        endepoch = startepoch + duration - 1
        tickshistory = await apiconnection.ticks_history(
            {
                "ticks_history": asset,
                "end": endepoch,
                "start": startepoch
            }
        )

        return tickshistory

if __name__ == "__main__":
    apiConnector = APIConnector()
    try:
        apiConnection = asyncio.run(apiConnector.create_api_connection())
        print(type(apiConnection))
    except socket.gaierror:
        print
