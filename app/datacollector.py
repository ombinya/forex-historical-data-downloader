"""
Contains the DataCollector class, which implements functions related to how data
is retrieved from the Deriv API and sent to a local database.
"""

from datetime import datetime
import asyncio

import deriv_api

from .databasemanager import DatabaseManager
from PyQt5.QtCore import QObject, pyqtSignal
from .apiconnector import APIConnector
import socket
from time import sleep


class DataCollector(QObject):
    finished = pyqtSignal()
    connectedtoapi = pyqtSignal(bool)
    createddb = pyqtSignal(bool)
    senttodb = pyqtSignal(int)
    downloadedsuccessfully = pyqtSignal()
    gotinvalidtimerange = pyqtSignal(str)

    def __init__(self, asset, startdatetime, enddatetime):
        super().__init__()

        self.asset = asset
        self.startdatetime = startdatetime
        self.enddatetime = enddatetime

        self.duration = 3600
        self.processes = 12
        self.loop = asyncio.new_event_loop()

        self.apiconnector = APIConnector()\

        datetimeformat = "%Y_%m_%d_%H_%M_%S"
        currentdatetime = datetime.now()
        datetimestring = currentdatetime.strftime(datetimeformat)
        dbfilename = self.asset + "_" + datetimestring + ".db"
        self.databasemanager = DatabaseManager(dbfilename, self.asset)
        self.percentagedownloaded = 0

    def run(self):
        asyncio.run(self.collect_data())
        self.finished.emit()

    async def connected_to_api(self):
        try:
            await self.apiconnector.create_api_connection()
            return True
        except socket.gaierror:
            return False

    async def created_db(self):

        try:
            await self.databasemanager.create_table()
            return True
        except:
            return False

    def got_invalid_time_range(self, a, b):
        if b <= a:
            return "End date-time must be later than inital date-time."
        elif b - a > 366 * 24 * 60 * 60:
            return "You can only download data of maximum range of one year at a time."

    async def collect_data(self):
        """
        Specifies the parameters of the data to be collected and sends this data to
        local database.
        """

        initialstartepoch = int(self.startdatetime.timestamp())
        finalendepoch = int(self.enddatetime.timestamp())

        invalidtimerangemessage = self.got_invalid_time_range(
            initialstartepoch, finalendepoch)

        if invalidtimerangemessage:
            self.gotinvalidtimerange.emit(invalidtimerangemessage)
            return

        self.connectedtoapi.emit(await self.connected_to_api())
        self.createddb.emit(await self.created_db())

        mainstartepoch = initialstartepoch

        while mainstartepoch < finalendepoch:
            startepochs = [mainstartepoch +
                           (i * self.duration) for i in range(self.processes)]

            results = None
            while not results:
                try:
                    tasks = [self.apiconnector.ticks_history(startepoch, self.duration, self.asset) for
                             startepoch in startepochs]
                    async with asyncio.timeout(10):
                        results = await asyncio.gather(*tasks)
                except deriv_api.ResponseError:
                    print("It's just a response error")
                    sleep(10)
                except TimeoutError:
                    print("Timeout error!")
                    print("Percentage downloaded:", self.percentagedownloaded)
                    sleep(5)
                    print("Retrying...")
                except Exception as e:
                    print(type(e).__name__, "\nFor data at",
                          datetime.fromtimestamp(mainstartepoch))
                    raise

            times = []
            prices = []

            for result in results:
                currenttimes = result["history"]["times"]
                currentprices = result["history"]["prices"]
                if len(currenttimes) > 0 and currenttimes[-1] > finalendepoch:
                    currenttimes = [
                        epoch for epoch in currenttimes if epoch <= finalendepoch]
                    currentprices = currentprices[: len(currenttimes)]

                times.extend(currenttimes)
                prices.extend(currentprices)

            if len(times) > 0:
                data = zip(times, prices)
                await self.databasemanager.insert_data(data)
                self.percentagedownloaded = ((times[-1] - initialstartepoch) /
                                             (finalendepoch - initialstartepoch)) * 100

                self.senttodb.emit(int(self.percentagedownloaded))

            mainstartepoch = mainstartepoch + (self.duration * self.processes)

        self.downloadedsuccessfully.emit()


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
