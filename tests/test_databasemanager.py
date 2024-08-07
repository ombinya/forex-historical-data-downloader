import unittest
import sys
import os
from datetime import datetime
from aiosqlite import connect

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

        self.dbfilepath = self.databasemanager.get_downloads_folder_path() + "/" + self.dbfilename

    async def test_create_table(self):
        await self.databasemanager.create_table()

        # Confirm that the database has been created successfully
        self.assertTrue(os.path.exists(self.dbfilepath))

        # Confirm that the db table has been created successfully
        async with connect(self.dbfilepath) as con:
            async with con.execute("SELECT name FROM sqlite_master WHERE type='table'") as cursor:
                tables = await cursor.fetchall()

            tablenames = [table[0] for table in tables]
            self.assertTrue(self.asset in tablenames)

    async def test_insert_data(self):

        await self.databasemanager.create_table()
        epochs = [1000 + i for i in range(10)]
        prices = [1.5 + (i * 0.01) for i in range(10)]

        data = zip(epochs, prices)
        datacopy = zip(epochs, prices)

        await self.databasemanager.insert_data(data)

        async with connect(self.dbfilepath) as con:
            async with con.execute("SELECT * FROM {}".format(self.asset)) as cursor:
                entries = await cursor.fetchall()

                self.assertEqual(list(datacopy), list(entries))

    def tearDown(self):
        # Delete database file after test
        os.remove(self.databasemanager.dbfilepath)
        assert not os.path.exists(self.dbfilepath)