import customtkinter
from tkcalendar import Calendar, DateEntry
from tktimepicker import SpinTimePickerOld, constants

class DateTimePickerWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__()
        self.overrideredirect(True)
        # self.geometry("400x300")
        self.center_on_parent(master)

        row = 0

        self.datetimepicker = Calendar(
            self, selectmode="day", date_pattern="y-mm-dd")
        self.datetimepicker.grid(
            row=row, column=0, padx=10, pady=(10, 0), sticky="")
        row += 1

        self.submitbutton = customtkinter.CTkButton(
            self, text="Submit", command=self.capture_new_date_time)
        self.submitbutton.grid(row=row, column=0, padx=10, pady=(10, 0), sticky="w")
        row += 1

    def capture_new_date_time(self):
        self.destroy()

    def center_on_parent(self, parent):
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        window_width = 400
        window_height = 300

        pos_x = parent_x + (parent_width // 2) - (window_width // 2)
        pos_y = parent_y + (parent_height // 2) - (window_height // 2)

        self.geometry(
            "{}x{}+{}+{}".format(window_width, window_height, pos_x, pos_y))


class PairOptionsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        row = 0

        self.pairoptionsmenulabel = customtkinter.CTkLabel(self, text="Currency Pair")
        self.pairoptionsmenulabel.grid(row=row, column=0, padx=10, pady=(10, 0), sticky="w")
        row += 1

        currencypairs = ["EURUSD", "EURCHF"]
        self.pairoptionsmenu = customtkinter.CTkOptionMenu(
            self, values=currencypairs, corner_radius=0)
        self.pairoptionsmenu.grid(
            row=row, column=0, padx=10, pady=(0, 0), sticky="w")
        row += 1

        self.datetimepickerlabel = customtkinter.CTkLabel(self, text="Date and Time")
        self.datetimepickerlabel.grid(
            row=row, column=0, padx=10, pady=(10, 0), sticky="w")
        row += 1

        self.startatlabel = customtkinter.CTkLabel(self, text="Start at:")
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

        self.endat = customtkinter.CTkLabel(self, text="End at:")
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

        self.downloadbutton = customtkinter.CTkButton(
            self,
            text="Download",
            corner_radius=0,
            command=self.download_data
        )
        self.downloadbutton.grid(
            row=row, column=0, padx=10, pady=(20, 0), sticky="w")
        row += 1

    def download_data(self):
        print("Downloading data...")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Shika Forex Data")
        self.geometry("600x360")
        self._set_appearance_mode("dark")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # self.checkbox_frame = MyCheckboxFrame(self)
        # self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nswe")

        self.pairoptionsframe = PairOptionsFrame(self)
        self.pairoptionsframe.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nswe")
        # self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        # self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        # self.button._background_corner_colors = ["grey" for i in range(4)]

    def button_callback(self):
        print("button pressed")


app = App()
app.mainloop()
