"""
Contains the DataCollector class, which implements functions related to how data
is retrieved from the Deriv API and sent to a local database.
"""

from datetime import datetime
import asyncio
import websockets
from deriv_api import DerivAPI
from databasemanager import DatabaseManager
from PyQt5.QtCore import QObject, pyqtSignal
from dotenv import load_dotenv
import os


class DataCollector(QObject):
    finished = pyqtSignal()
    connectedtoapi = pyqtSignal(bool)
    createddb = pyqtSignal(bool)
    downloaded = pyqtSignal(bool)

    def __init__(self, asset, startdatetime, enddatetime):
        super().__init__()

        self.asset = asset
        self.startdatetime = startdatetime
        self.enddatetime = enddatetime

        self.duration = 3600  # Number of seconds in an hour
        self.processes = 12
        self.loop = asyncio.new_event_loop()

    def run(self):
        asyncio.run(self.collect_data())
        self.finished.emit()

    async def create_api_connection(self):
        """
        Creates a connection to the DERIV API.
        """

        load_dotenv()
        derivappid = os.environ.get("DERIV_APP_ID")

        connection = await websockets.connect(
            'wss://ws.derivws.com/websockets/v3?app_id={}'.format(derivappid)
        )

        self.apiconnection = DerivAPI(connection=connection)

    async def get_asset_index(self):
        try:
            assets = await self.apiconnection.asset_index({"asset_index": 1})
            return assets
        except Exception as e:
            print(type(e).__name__, "----- Trouble getting asset index")
            print("Error message ->", e)

    async def ticks_history(self, startepoch):
        """
        Retrieves historical tick data for a given asset, from the start epoch to the end epoch.

        :param startepoch: the start epoch
        :return: dictionary object containing the retrieved forex data
        """

        endepoch = startepoch + self.duration - 1
        tickshistory = await self.apiconnection.ticks_history(
            {
                "ticks_history": self.asset,
                "end": endepoch,
                "start": startepoch
            }
        )

        return tickshistory

    async def collect_data(self):
        """
        Specifies the paramaters of the data to be collected and sends this data to
        local database.
        """

        try:
            await self.create_api_connection()
            self.connectedtoapi.emit(True)
        except:
            self.connectedtoapi.emit(False)
            return

        datetimeformat = "%Y_%m_%d_%H_%M_%S"
        currentdatetime = datetime.now()
        datetimestring = currentdatetime.strftime(datetimeformat)
        dbfilename = self.asset + "_" + datetimestring + ".db"

        try:
            databasemanager = DatabaseManager(dbfilename, self.asset)
            await databasemanager.create_table()
            self.createddb.emit(True)
        except:
            self.createddb.emit(False)
            return

        mainstartepoch = int(self.startdatetime.timestamp())
        finalendepoch = int(self.enddatetime.timestamp())

        while mainstartepoch < finalendepoch:
            startepochs = [mainstartepoch + (i * self.duration) for i in range(self.processes)]
            tasks = [self.ticks_history(startepoch) for startepoch in startepochs]
            results = await asyncio.gather(*tasks)

            times = []
            prices = []

            for result in results:
                currenttimes = result["history"]["times"]
                currentprices = result["history"]["prices"]
                if len(currenttimes) > 0 and currenttimes[-1] > finalendepoch:
                    currenttimes = [epoch for epoch in currenttimes if epoch <= finalendepoch]
                    currentprices = currentprices[ : len(currenttimes)]

                times.extend(currenttimes)
                prices.extend(currentprices)

            try:
                data = zip(times, prices)
            except Exception as e:
                print(f"Exception during zipping: {e}")
                print("Chunk size", len(times))

            if len(times) > 0:
                await databasemanager.insert_data(data)

            mainstartepoch = mainstartepoch + (self.duration * self.processes)


if __name__ == "__main__":
    async def main():
        dataCollector = DataCollector(None, None, None)
        await dataCollector.create_api_connection()
        assets = await dataCollector.get_asset_index()

        tradeitems = []
        tradeitemsdisplay = []

        for asset in assets["asset_index"]:
            tradeitems.append(asset[0])
            tradeitemsdisplay.append(asset[1])

        print(tradeitemsdisplay)

    asyncio.run(main())