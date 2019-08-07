# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/printwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SerialWindow(object):
    def setupUi(self, SerialWindow):
        SerialWindow.setObjectName("SerialWindow")
        SerialWindow.resize(800, 480)
        SerialWindow.setMaximumSize(QtCore.QSize(800, 480))
        self.Back = QtWidgets.QPushButton(SerialWindow)
        self.Back.setGeometry(QtCore.QRect(10, 380, 91, 91))
        self.Back.setMaximumSize(QtCore.QSize(100, 100))
        self.Back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon)
        self.Back.setIconSize(QtCore.QSize(100, 100))
        self.Back.setObjectName("Back")
        self.tabWidget = QtWidgets.QTabWidget(SerialWindow)
        self.tabWidget.setGeometry(QtCore.QRect(0, 40, 801, 301))
        self.tabWidget.setObjectName("tabWidget")
        self.SD = QtWidgets.QWidget()
        self.SD.setObjectName("SD")
        self.widget = QtWidgets.QWidget(self.SD)
        self.widget.setGeometry(QtCore.QRect(650, 20, 111, 231))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ScanSD = QtWidgets.QPushButton(self.widget)
        self.ScanSD.setMaximumSize(QtCore.QSize(100, 100))
        self.ScanSD.setObjectName("ScanSD")
        self.verticalLayout.addWidget(self.ScanSD)
        self.StartPrint = QtWidgets.QPushButton(self.widget)
        self.StartPrint.setMaximumSize(QtCore.QSize(100, 100))
        self.StartPrint.setObjectName("StartPrint")
        self.verticalLayout.addWidget(self.StartPrint)
        self.FileList = QtWidgets.QTableWidget(self.SD)
        self.FileList.setGeometry(QtCore.QRect(60, 20, 571, 231))
        self.FileList.setObjectName("FileList")
        self.FileList.setColumnCount(1)
        self.FileList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.FileList.setHorizontalHeaderItem(0, item)
        self.tabWidget.addTab(self.SD, "")
        self.USB = QtWidgets.QWidget()
        self.USB.setObjectName("USB")
        self.tabWidget.addTab(self.USB, "")
        self.ScanSD_2 = QtWidgets.QPushButton(SerialWindow)
        self.ScanSD_2.setGeometry(QtCore.QRect(660, 360, 100, 91))
        self.ScanSD_2.setMaximumSize(QtCore.QSize(100, 100))
        self.ScanSD_2.setObjectName("ScanSD_2")

        self.retranslateUi(SerialWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SerialWindow)

    def retranslateUi(self, SerialWindow):
        _translate = QtCore.QCoreApplication.translate
        SerialWindow.setWindowTitle(_translate("SerialWindow", "ControlWindow"))
        self.ScanSD.setText(_translate("SerialWindow", "Scan SD"))
        self.StartPrint.setText(_translate("SerialWindow", "Start Print"))
        item = self.FileList.horizontalHeaderItem(0)
        item.setText(_translate("SerialWindow", "File"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SD), _translate("SerialWindow", "SD"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.USB), _translate("SerialWindow", "USB"))
        self.ScanSD_2.setText(_translate("SerialWindow", "Active Print"))

