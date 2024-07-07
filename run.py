"""
This script serves as the entry point for running the main functionality of the program.
"""

import os
import asyncio
from databasemanager import DatabaseManager
from datacollector import DataCollector


async def main():
    """ Initializes the DataCollector, sets up the connection to the Deriv API,
    and starts collecting data.
    """

    databaseManager = DatabaseManager("forex-data.db")
    # await databaseManager.create_table()

    # Provide the App ID
    appid = os.environ["DERIV_APP_ID"]

    dataCollector = DataCollector(databaseManager, appid)
    await dataCollector.create_api_connection()
    await dataCollector.collect_data()


asyncio.run(main())
