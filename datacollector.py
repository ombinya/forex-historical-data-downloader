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

    async def ticks_history(self, startepoch):
        """
        Retrieves Forex data for the specified currency pair, from the start epoch to the end epoch.

        :param startepoch: the start epoch
        :return: dictionary object containing the retrieved forex data
        """

        endepoch = startepoch + self.duration - 1
        tickshistory = await self.apiconnection.ticks_history(
            {
                "ticks_history": "frxEURUSD",
                "end": endepoch,
                "start": startepoch
            }
        )

        return tickshistory

    async def collect_data(self):
        """
        Specifies the paramaters of the data to be collected and sends this data to local database.
        """
        try:
            lastEpoch = await self.databasemanager.last_epoch()
            mainstartepoch = lastEpoch + 1
        except:
            mainstartepoch = int(datetime(2022, 1, 1, 0, 0).timestamp())

        while datetime.fromtimestamp(mainstartepoch).year < 2024:
            startepochs = [mainstartepoch + (i * self.duration) for i in range(self.processes)]
            tasks = [self.ticks_history(startepoch) for startepoch in startepochs]
            results = await asyncio.gather(*tasks)

            times = []
            prices = []
            for result in results:
                times.extend(result["history"]["times"])
                prices.extend(result["history"]["prices"])

            data = zip(times, prices)

            endepoch = mainstartepoch + (self.duration * self.processes) - 1
            print("Inserting data for",
                  datetime.fromtimestamp(mainstartepoch), "-",
                  datetime.fromtimestamp(endepoch), end=" ")
            await self.databasemanager.insert_data(data)
            print("DONE")

            mainstartepoch = mainstartepoch + (self.duration * self.processes)


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
