# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Designer UI Files/appdesign.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(243, 384)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TRADE_ITEMS = QtWidgets.QComboBox(self.centralwidget)
        self.TRADE_ITEMS.setGeometry(QtCore.QRect(20, 60, 91, 22))
        self.TRADE_ITEMS.setObjectName("TRADE_ITEMS")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 61, 16))
        self.label.setObjectName("label")
        self.DOWNLOAD_BUTTON = QtWidgets.QPushButton(self.centralwidget)
        self.DOWNLOAD_BUTTON.setGeometry(QtCore.QRect(20, 220, 201, 31))
        self.DOWNLOAD_BUTTON.setStyleSheet("background-color: rgb(95, 75, 140);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.DOWNLOAD_BUTTON.setObjectName("DOWNLOAD_BUTTON")
        self.START_DATE = QtWidgets.QDateEdit(self.centralwidget)
        self.START_DATE.setGeometry(QtCore.QRect(20, 120, 91, 22))
        self.START_DATE.setCalendarPopup(True)
        self.START_DATE.setObjectName("START_DATE")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 111, 16))
        self.label_2.setObjectName("label_2")
        self.START_TIME = QtWidgets.QTimeEdit(self.centralwidget)
        self.START_TIME.setGeometry(QtCore.QRect(130, 120, 91, 22))
        self.START_TIME.setObjectName("START_TIME")
        self.END_DATE = QtWidgets.QDateEdit(self.centralwidget)
        self.END_DATE.setGeometry(QtCore.QRect(20, 180, 91, 22))
        self.END_DATE.setCalendarPopup(True)
        self.END_DATE.setObjectName("END_DATE")
        self.END_TIME = QtWidgets.QTimeEdit(self.centralwidget)
        self.END_TIME.setGeometry(QtCore.QRect(130, 180, 91, 22))
        self.END_TIME.setObjectName("END_TIME")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 160, 111, 16))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 243, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Trade Item"))
        self.DOWNLOAD_BUTTON.setText(_translate("MainWindow", "DOWNLOAD DATA"))
        self.START_DATE.setDisplayFormat(_translate("MainWindow", "dd-MM-yyyy"))
        self.label_2.setText(_translate("MainWindow", "Start Date and Time"))
        self.START_TIME.setDisplayFormat(_translate("MainWindow", "hh:mm"))
        self.END_DATE.setDisplayFormat(_translate("MainWindow", "dd-MM-yyyy"))
        self.label_3.setText(_translate("MainWindow", "End Date and Time"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

