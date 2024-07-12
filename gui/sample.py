import customtkinter
from tkcalendar import Calendar

class PairOptionsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        row = 0

        self.pairoptionsmenulabel = customtkinter.CTkLabel(self, text="Select Currency Pair")
        self.pairoptionsmenulabel.grid(row=row, column=0, padx=10, pady=(10, 0), sticky="w")
        row += 1

        currencypairs = ["EURUSD", "EURCHF"]
        self.pairoptionsmenu = customtkinter.CTkOptionMenu(self, values=currencypairs)
        self.pairoptionsmenu.grid(row=row, column=0, padx=10, pady=(10, 0), sticky="w")
        row += 1

        self.datetimepickerlabel = customtkinter.CTkLabel(self, text="Pick Date and Time")
        self.datetimepickerlabel.grid(row=row, column=0, padx=10, pady=(10, 0), sticky="w")
        row += 1

        self.datetimepicker = Calendar(self, selectmode="day", date_pattern="y-mm-dd")
        self.datetimepicker.grid(row=row, column=0, padx=10, pady=(10, 0), sticky="w")


# class MyCheckboxFrame(customtkinter.CTkFrame):
#     def __init__(self, master):
#         super().__init__(master)
#
#         self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
#         self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
#         self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
#         self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("1080x480")
        self._set_appearance_mode("dark")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # self.checkbox_frame = MyCheckboxFrame(self)
        # self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nswe")

        self.pairoptionsframe = PairOptionsFrame(self)
        self.pairoptionsframe.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nswe")
        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.button._background_corner_colors = ["grey" for i in range(4)]

        print(self.button._background_corner_colors)

    def button_callback(self):
        print("button pressed")


app = App()
app.mainloop()
