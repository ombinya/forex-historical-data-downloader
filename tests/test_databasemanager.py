import unittest
import sys
import os
from datetime import datetime

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.databasemanager import DatabaseManager

class TestDatabaseManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.asset = "asset"

        datetimeformat = "%Y_%m_%d_%H_%M_%S"
        currentdatetime = datetime.now()
        datetimestring = currentdatetime.strftime(datetimeformat)
        self.dbfilename = self.asset + "_" + datetimestring + ".db"
        self.databasemanager = DatabaseManager(self.dbfilename, self.asset)

    async def test_create_table(self):
        await self.databasemanager.create_table()
        dbfilepath = self.databasemanager.get_downloads_folder_path() + "/" + self.dbfilename

        self.assertTrue(os.path.exists(dbfilepath))

    def tearDown(self):
        # Delete database file after test
        os.remove(self.databasemanager.dbfilepath)