from qtgui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QDate
import sys
import appvars
from datetime import datetime, date, timedelta
from datacollector import DataCollector


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread = None

    def set_thread(self, thread, dataCollector):
        self.thread = thread

    def closeEvent(self, event):
        # if self.thread:
        #     try:
        #         if self.thread.isRunning():
        #             print("Thread is running, attempting to quit and wait")
        #             try:
        #                 self.thread.quit()
        #                 self.thread.wait()
        #             except Exception as e1:
        #                 print(f"Exception during thread quit/wait: {e1}")
        #         else:
        #             print("Thread is not running")
        #     except Exception as e2:
        #         print(f"Exception while checking if thread is running: {e2.__class__.__name__}: {e2}")
        # else:
        #     print("No thread to quit")
        event.accept()


class GUIManager(Ui_MainWindow):
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = MainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.ui.DOWNLOAD_BUTTON.clicked.connect(self.download_init)

    def set_defaults(self):
        self.ui.TRADE_ITEMS.addItems(appvars.tradeitems)
        self.ui.START_DATE.setDate(date.today() - timedelta(days=1))
        self.ui.END_DATE.setDate(date.today())

    def download_init(self):
        self.ui.DOWNLOAD_BUTTON.setEnabled(False)

        self.tradeitem = self.ui.TRADE_ITEMS.currentText()

        startdate = self.ui.START_DATE.date().toPyDate()
        starttime = self.ui.START_TIME.time().toPyTime()
        self.startdatetime = datetime.combine(startdate, starttime)

        enddate = self.ui.END_DATE.date().toPyDate()
        endtime = self.ui.END_TIME.time().toPyTime()
        self.enddatetime = datetime.combine(enddate, endtime)

        self.thread = QThread()
        self.dataCollector = DataCollector(self.tradeitem, self.startdatetime, self.enddatetime)
        self.dataCollector.moveToThread(self.thread)

        self.thread.started.connect(self.dataCollector.run)
        print("Quitting self.thread")
        self.dataCollector.finished.connect(self.thread.quit)
        print("Will delete datacollector later")
        self.dataCollector.finished.connect(self.dataCollector.deleteLater)
        print("I'll delete later")
        self.thread.finished.connect(self.thread.deleteLater)
        print("About to activate the button")
        self.thread.finished.connect(self.on_thread_finished)
        print("Button activated")
        self.MainWindow.set_thread(self.thread, self.dataCollector)
        self.thread.start()

    def on_thread_finished(self):
        print("Inside on_thread_finished function")
        self.ui.DOWNLOAD_BUTTON.setEnabled(True)

        # print("1")
        # if self.thread:
        #     print("Thread exists")
        #     if self.thread.isRunning():
        #         print("Quitting")
        #         self.thread.quit()
        #         print("waiting")
        #         self.thread.wait()
        # print("2")

    def get_date_time(self, datestring, timeitems):
        datetimeformat = "%Y-%m-%d %H:%M:%S"
        hour, minute = timeitems[:2]
        timestring = self.two_digit_string(hour) + ":" + self.two_digit_string(minute) + ":00"
        datetimestring = str(datestring) + " " + timestring
        datetimeobj = datetime.strptime(datetimestring, datetimeformat)

        return datetimeobj

    def show_gui(self):
        self.MainWindow.show()

    def close_gui(self):
        # self.exit()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    def main():
        guimanager = GUIManager()
        guimanager.set_defaults()
        guimanager.show_gui()
        guimanager.close_gui()

    main()
