"""
Contains the DataCollector class, which implements functions related to how data
is retrieved from the Deriv API and sent to a local database.
"""

from datetime import datetime
import asyncio
from databasemanager import DatabaseManager
from PyQt5.QtCore import QObject, pyqtSignal
from apiconnector import APIConnector


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

        self.apiconnector = APIConnector()

    def run(self):
        asyncio.run(self.collect_data())
        self.finished.emit()

    async def collect_data(self):
        """
        Specifies the parameters of the data to be collected and sends this data to
        local database.
        """

        initialstartepoch = int(self.startdatetime.timestamp())
        finalendepoch = int(self.enddatetime.timestamp())

        if finalendepoch <= initialstartepoch:
            self.gotinvalidtimerange.emit("End date-time must be later than inital date-time.")
            return
        elif finalendepoch - initialstartepoch > 366 * 24 * 60 * 60:
            self.gotinvalidtimerange.emit("You can only download data of maximum range of one year at a time.")
            return

        try:
            await self.apiconnector.create_api_connection()
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

        mainstartepoch = initialstartepoch

        while mainstartepoch < finalendepoch:
            startepochs = [mainstartepoch + (i * self.duration) for i in range(self.processes)]
            tasks = [self.apiconnector.ticks_history(startepoch, self.duration, self.asset) for
                     startepoch in startepochs]

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
                print("Exception during zipping: {}".format(e))
                print("Chunk size", len(times))

            if len(times) > 0:
                await databasemanager.insert_data(data)
                percentagedownloaded = ((times[-1] - initialstartepoch) / \
                             (finalendepoch - initialstartepoch)) * 100

                self.senttodb.emit(int(percentagedownloaded))

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