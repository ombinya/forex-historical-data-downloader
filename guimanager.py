from qtgui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
import sys
from datetime import datetime, date, timedelta
from datacollector import DataCollector


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread = None

    def set_thread(self, thread):
        self.thread = thread

    def closeEvent(self, event):
        event.accept()


class GUIManager(Ui_MainWindow):
    def __init__(self, assets):
        self.assets = assets

        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = MainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.ui.DOWNLOAD_BUTTON.clicked.connect(self.download_init)

    def set_defaults(self):
        self.ui.ASSET_OPTIONS.addItems(self.assets.keys())
        self.ui.START_DATE.setDate(date.today() - timedelta(days=1))
        self.ui.END_DATE.setDate(date.today())

    def download_init(self):
        self.ui.DOWNLOAD_BUTTON.setEnabled(False)
        self.assetid = self.assets[self.ui.ASSET_OPTIONS.currentText()]

        startdate = self.ui.START_DATE.date().toPyDate()
        starttime = self.ui.START_TIME.time().toPyTime()
        self.startdatetime = datetime.combine(startdate, starttime)

        enddate = self.ui.END_DATE.date().toPyDate()
        endtime = self.ui.END_TIME.time().toPyTime()
        self.enddatetime = datetime.combine(enddate, endtime)

        self.thread = QThread()
        self.dataCollector = DataCollector(self.assetid, self.startdatetime, self.enddatetime)
        self.dataCollector.moveToThread(self.thread)

        self.thread.started.connect(self.dataCollector.run)
        self.dataCollector.finished.connect(self.thread.quit)
        self.dataCollector.finished.connect(self.dataCollector.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.on_thread_finished)
        self.MainWindow.set_thread(self.thread)
        self.thread.start()

    def on_thread_finished(self):
        self.ui.DOWNLOAD_BUTTON.setEnabled(True)

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
        sys.exit(self.app.exec())


if __name__ == "__main__":
    def main():
        guimanager = GUIManager()
        guimanager.set_defaults()
        guimanager.show_gui()
        guimanager.close_gui()

    main()
