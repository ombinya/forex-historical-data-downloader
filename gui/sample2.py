import tkinter as tk
from tktimepicker import AnalogPicker, AnalogThemes, SpinTimePickerOld, constants
# note: you can also make use of mouse wheel or keyboard to scroll or enter the spin timepicker
root = tk.Tk()

time_picker = SpinTimePickerOld(root, orient=constants.HORIZONTAL)
time_picker.addAll(constants.HOURS24)  # adds hours clock, minutes and period
time_picker.pack(expand=True, fill="both")

# theme = AnalogThemes(time_picker)
# theme.setDracula()

root.mainloop()