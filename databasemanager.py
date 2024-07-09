"""
Contains the DatabaseManager class, which implements the functions related to a local database.
"""
from aiosqlite import connect
import asyncio


class DatabaseManager:
    def __init__(self, dbfilename):
        self.dbfilename = dbfilename

    async def create_table(self):
        """
        Creates a new database table. It contains a check to prevent accidental loss of data.
        """

        while True:
            choice = input("Do you want to recreate the database table? (y/n) ")

            if choice == "y":
                break
            elif choice == "n":
                return
            else:
                print("Input must be 'y' or 'n'. Try again...")
                continue

        async with connect(self.dbfilename) as con:
            await con.execute("""DROP TABLE IF EXISTS EURUSD_raw""")
            await con.execute("""
                CREATE TABLE IF NOT EXISTS EURUSD_raw(
                    epoch INTEGER,
                    average REAL
                )
            """)

            await con.commit()

    async def insert_data(self, data):
        """
        Inserts data from a zip object into a local database. Each tuple in the zip object
        corresponds to a row in the table.

        :param data: zip object containing forex data
        """

        async with connect(self.dbfilename) as con:
            await con.executemany("""
                INSERT INTO EURUSD_raw
                VALUES (?,?)
            """, data)

            await con.commit()

    async def last_epoch(self):
        """
        Retrieves the latest value in the epoch column of the database.
        :return: integer representing the latest epoch in the database
        """

        async with connect(self.dbfilename) as con:
            selection = await con.execute("""
                SELECT epoch
                FROM EURUSD_raw
                ORDER BY epoch DESC 
                LIMIT 1
            """)

            lastepoch = (await selection.fetchone())[0]

            return lastepoch


if __name__ == "__main__":


    async def main():
        """
        Function to test the module.
        """

        dbm = DatabaseManager("test.db")
        await dbm.create_table()
        print(dbm.last_epoch.__doc__)

    asyncio.run(main())