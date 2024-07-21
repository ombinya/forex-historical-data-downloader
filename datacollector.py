"""
Contains the DataCollector class, which implements functions related to how data
is retrieved from the Deriv API and sent to a local database.
"""

import os
from datetime import datetime
import asyncio
import websockets
from deriv_api import DerivAPI
from databasemanager import DatabaseManager
import appvars


class DataCollector:
    def __init__(self, databasemanager, appid):
        self.databasemanager = databasemanager
        self.appid = appid  # App ID
        self.duration = 3600  # Number of seconds in an hour
        self.processes = 12

    async def create_api_connection(self):
        """
        Creates a connection to the DERIV API.
        """

        connection = await websockets.connect(
            'wss://ws.derivws.com/websockets/v3?app_id={}'.format(self.appid)
        )

        self.apiconnection = DerivAPI(connection=connection)

    async def ticks_history(self, startepoch, pair):
        """
        Retrieves Forex data for the specified currency pair, from the start epoch to the end epoch.

        :param startepoch: the start epoch
        :return: dictionary object containing the retrieved forex data
        """

        endepoch = startepoch + self.duration - 1
        commodity = "frx" + pair
        tickshistory = await self.apiconnection.ticks_history(
            {
                "ticks_history": commodity,
                "end": endepoch,
                "start": startepoch
            }
        )

        return tickshistory

    async def collect_data(self, pair, startdatetime, enddatetime):
        """
        Specifies the paramaters of the data to be collected and sends this data to local database.
        """

        print("Initializing data collection...")

        mainstartepoch = int(startdatetime.timestamp())
        finalendepoch = int(enddatetime.timestamp())

        while appvars.running == True and mainstartepoch < finalendepoch:
            startepochs = [mainstartepoch + (i * self.duration) for i in range(self.processes)]
            tasks = [self.ticks_history(startepoch, pair) for startepoch in startepochs]
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

            data = zip(times, prices)

            await self.databasemanager.insert_data(data)

            mainstartepoch = mainstartepoch + (self.duration * self.processes)

        appvars.downloading = False
        print("Download Complete!")


if __name__ == "__main__":
    async def main():
        appid = os.environ["DERIV_APP_ID"]
        databasemanager = DatabaseManager("test.db")
        await databasemanager.create_table()
        dataCollector = DataCollector(databasemanager, appid)
        await dataCollector.create_api_connection()

        await dataCollector.collect_data()

    startTime = datetime.now()
    asyncio.run(main())
    print("Time elapsed:", datetime.now() - startTime)
