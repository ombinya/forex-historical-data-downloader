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

        try:
            self.downloadprogressloglayout = QtWidgets.QVBoxLayout(self.ui.scrollAreaWidgetContents)
            self.downloadprogressloglayout.setContentsMargins(0, 0, 0, 0)  # Set margins to zero
            self.downloadprogressloglayout.setSpacing(0)
            self.ui.scrollAreaWidgetContents.setLayout(self.downloadprogressloglayout)
        except Exception as e:
            print(e)
        
        self.loglabels = []

    def set_defaults(self):
        self.ui.ASSET_OPTIONS.addItems(self.assets.keys())
        self.ui.START_DATE.setDate(date.today() - timedelta(days=1))
        self.ui.END_DATE.setDate(date.today())

    def download_init(self):
        self.ui.DOWNLOAD_BUTTON.setEnabled(False)
        self.clear_log()

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

        self.dataCollector.connectedtoapi.connect(self.on_api_connection)
        self.dataCollector.createddb.connect(self.on_db_creation)
        self.dataCollector.senttodb.connect(self.on_sent_to_db)
        self.dataCollector.downloadedsuccessfully.connect(self.on_downloaded_successfully)
        self.dataCollector.gotinvalidtimerange.connect(self.on_got_invalid_time_range)
        self.dataCollector.finished.connect(self.thread.quit)
        self.dataCollector.finished.connect(self.dataCollector.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.on_thread_finished)
        self.MainWindow.set_thread(self.thread)
        self.thread.start()

    def clear_log(self):
        for label in self.loglabels:
            try:
                self.downloadprogressloglayout.removeWidget(label)
                label.deleteLater()
            except Exception as e:
                print("Error while clearing log: ", e)

    def on_api_connection(self, connected):
        if connected:
            message = "Connected to DERIV API successfully."
            messagetype = "primary"
        else:
            message = "Could not connect to DERIV API. Check your Internet connection."
            messagetype = "danger"

        self.add_to_log(message, messagetype)

    def on_db_creation(self, created):
        if created:
            message = "Database created successfully."
            messagetype = "primary"
        else:
            message = "Failed to create database."
            messagetype = "danger"

        self.add_to_log(message, messagetype)

    def on_got_invalid_time_range(self, message):
        self.clear_log()
        self.add_to_log("Error: Invalid time range", "danger")
        self.add_to_log("Reason: {}".format(message), "danger")

    def on_sent_to_db(self, percentagedownloaded):
        if "Downloading..." in self.loglabels[-1].text():
            label = self.loglabels.pop()
            label.deleteLater()

        self.add_to_log("Downloading... {}%".format(percentagedownloaded), "primary")

    def on_downloaded_successfully(self):
        self.clear_log()
        self.add_to_log("Download complete!", "primary")

    def on_thread_finished(self):
        self.ui.DOWNLOAD_BUTTON.setEnabled(True)

    def add_to_log(self, message, messagetype=None):
        label = QtWidgets.QLabel(message)
        label.setContentsMargins(0, 0, 0, 0)
        if messagetype == "danger":
            label.setStyleSheet("color: rgb(255, 0, 0);")
        elif messagetype == "primary":
            label.setStyleSheet("color: rgb(230, 150, 140);")

        self.downloadprogressloglayout.addWidget(label)
        self.loglabels.append(label)

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
