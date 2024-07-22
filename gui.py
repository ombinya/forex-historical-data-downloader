import asyncio
import customtkinter as ctk
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerOld, constants
from databasemanager import DatabaseManager
from datacollector import DataCollector
import os
import appvars
from datetime import datetime


class BigFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        row = 0

        self.pairoptionsmenulabel = ctk.CTkLabel(self, text="Currency Pair")
        self.pairoptionsmenulabel.grid(row=row, column=0, padx=10, pady=(10, 0), sticky="w")
        row += 1

        currencypairs = ["AUDJPY", "AUDUSD", "EURAUD", "EURCAD", "EURCHF",
                         "EURGBP", "EURJPY", "EURUSD", "GBPAUD", "GBPJPY",
                         "GBPUSD", "USDCAD", "USDCHF", "USDJPY", "AUDCAD",
                         "AUDCHF", "AUDNZD", "EURNZD", "GBPCAD", "GBPCHF",
                         "GBPNOK", "GBPNZD", "NZDJPY", "NZDUSD", "USDMXN",
                         "USDNOK", "USDPLN", "USDSEK"]
        self.pairoptionsmenu = ctk.CTkOptionMenu(
            self, values=currencypairs, corner_radius=0, width=110)
        self.pairoptionsmenu.grid(
            row=row, column=0, padx=10, pady=(0, 0), sticky="w")
        row += 1

        self.datetimepickerlabel = ctk.CTkLabel(self, text="Date and Time")
        self.datetimepickerlabel.grid(
            row=row, column=0, padx=10, pady=(10, 0), sticky="w")
        row += 1

        self.startatlabel = ctk.CTkLabel(self, text="Start at:")
        self.startatlabel.grid(
            row=row, column=0, padx=10, pady=(0, 0), sticky="w")
        row += 1

        self.startdateentry = DateEntry(self, date_pattern="y-mm-dd")
        self.startdateentry.grid(
            row=row, column=0, padx=10, pady=(0, 0), sticky="w")
        row += 1

        self.starttimeentry = SpinTimePickerOld(
            self, orient=constants.HORIZONTAL)
        self.starttimeentry.addAll(constants.HOURS24)  # adds hours clock, minutes and period
        self.starttimeentry.configureAll(width=4)
        self.starttimeentry.grid(
            row=row, column=0, padx=10, pady=(10, 0), sticky="w")
        row += 1

        self.endat = ctk.CTkLabel(self, text="End at:")
        self.endat.grid(
            row=row, column=0, padx=10, pady=(10, 0), sticky="w")
        row += 1

        self.enddateentry = DateEntry(self, date_pattern="y-mm-dd")
        self.enddateentry.grid(row=row, column=0, padx=10, pady=(0, 0), sticky="w")
        row += 1

        self.endtimeentry = SpinTimePickerOld(
            self, orient=constants.HORIZONTAL)
        self.endtimeentry.addAll(constants.HOURS24)  # adds hours clock, minutes and period
        self.endtimeentry.configureAll(width=4)
        self.endtimeentry.grid(
            row=row, column=0, padx=10, pady=(10, 0), sticky="w")
        row += 1

        self.downloadbutton = ctk.CTkButton(
            self,
            text="Download",
            corner_radius=0,
            command=self.start_task
        )

        self.downloadbutton.grid(
            row=row, column=0, padx=10, pady=(20, 0), sticky="w")
        row += 1

    async def long_running_task(self, pair, startdatetime, enddatetime):
        """Initializes the DataCollector, sets up the connection to the Deriv API, and starts collecting data."""

        datetimeformat = "%Y_%m_%d_%H_%M_%S"

        currentdatetime = datetime.now()
        datetimestring = currentdatetime.strftime(datetimeformat)
        dbfilename = pair.lower() + "_" + datetimestring + ".db"
        databaseManager = DatabaseManager(dbfilename, pair)
        await databaseManager.create_table()

        appid = os.environ["DERIV_APP_ID"]

        dataCollector = DataCollector(databaseManager, appid)
        await dataCollector.create_api_connection()
        await dataCollector.collect_data(pair, startdatetime, enddatetime)

        if not appvars.downloading:
            self.downloadbutton.configure(state="enabled")

    def start_task(self):
        pair = self.pairoptionsmenu.get()

        startdate = self.startdateentry.get_date()
        starttime = self.starttimeentry.time()  # Assuming this returns a datetime.time object
        startdatetime = self.get_date_time(startdate, starttime)

        enddate = self.enddateentry.get_date()
        endtime = self.endtimeentry.time()  # Assuming this returns a datetime.time object
        enddatetime = self.get_date_time(enddate, endtime)

        appvars.downloading = True
        if appvars.downloading:
            self.downloadbutton.configure(state="disabled")

        asyncio.ensure_future(self.long_running_task(pair, startdatetime, enddatetime))

    def two_digit_string(self, num):
        twodigitstring = ""
        if num < 10:
            twodigitstring += "0" + str(num)
        else:
            twodigitstring += str(num)

        return twodigitstring

    def get_date_time(self, datestring, timeitems):
        datetimeformat = "%Y-%m-%d %H:%M:%S"
        hour, minute = timeitems[:2]
        timestring = self.two_digit_string(hour) + ":" + self.two_digit_string(minute) + ":00"
        datetimestring = str(datestring) + " " + timestring
        datetimeobj = datetime.strptime(datetimestring, datetimeformat)

        return datetimeobj

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Shika Forex Data")
        self.root.geometry("600x360")
        self.root._set_appearance_mode("dark")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        appvars.running = True
        row = 0

        self.bigframe = BigFrame(root)
        self.bigframe.grid(row=row, column=0, padx=10, pady=(10, 10), sticky="nswe")
        row += 1

        self.loop = asyncio.get_event_loop()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        appvars.running = False
        self.cancel_tasks()
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.root.quit()
        self.root.destroy()

    def cancel_tasks(self):
        """Cancel all pending tkinter tasks."""
        for task in self.root.tk.call('after', 'info'):
            self.root.after_cancel(task)


def main():
    ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

    root = ctk.CTk()
    app = App(root)

    async def main_loop():
        while appvars.running:
            app.root.update()
            await asyncio.sleep(0.01)

    asyncio.run(main_loop())


if __name__ == "__main__":
    main()