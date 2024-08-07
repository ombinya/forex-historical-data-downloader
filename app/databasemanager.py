"""
Contains the DatabaseManager class, which implements the functions related to a local database.
"""
from aiosqlite import connect
import asyncio
import winreg


class DatabaseManager:
    def __init__(self, dbfilename, pair):
        self.dbfilename = dbfilename
        self.dbfilepath = self.get_downloads_folder_path() + "/" + self.dbfilename
        self.pair = pair

        
    async def create_table(self):
        """
        Creates a new database table. It contains a check to prevent accidental loss of data.
        """

        async with connect(self.dbfilepath) as con:
            await con.execute("""DROP TABLE IF EXISTS {}""".format(self.pair))
            await con.execute("""
                CREATE TABLE IF NOT EXISTS {}(
                    epoch INTEGER,
                    average REAL
                )
            """.format(self.pair))

            await con.commit()

    async def insert_data(self, data):
        """
        Inserts data from a zip object into a local database. Each tuple in the zip object
        corresponds to a row in the table.

        :param data: zip object containing forex data
        """

        async with connect(self.dbfilepath) as con:
            await con.executemany("""
                INSERT INTO {}
                VALUES (?,?)
            """.format(self.pair), data)

            await con.commit()

    def get_downloads_folder_path(self):
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
        downloads_path = winreg.QueryValueEx(reg_key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
        winreg.CloseKey(reg_key)

        return downloads_path


if __name__ == "__main__":

    async def main():
        """
        Function to test the module.
        """

        dbm = DatabaseManager("test.db")
        await dbm.create_table()

    asyncio.run(main())