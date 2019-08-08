# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/printwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PrintWindow(object):
    def setupUi(self, PrintWindow):
        PrintWindow.setObjectName("PrintWindow")
        PrintWindow.resize(800, 480)
        PrintWindow.setMaximumSize(QtCore.QSize(800, 480))
        self.Back = QtWidgets.QPushButton(PrintWindow)
        self.Back.setGeometry(QtCore.QRect(10, 380, 91, 91))
        self.Back.setMaximumSize(QtCore.QSize(100, 100))
        self.Back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon)
        self.Back.setIconSize(QtCore.QSize(100, 100))
        self.Back.setObjectName("Back")
        self.tabWidget = QtWidgets.QTabWidget(PrintWindow)
        self.tabWidget.setGeometry(QtCore.QRect(0, 40, 801, 301))
        self.tabWidget.setObjectName("tabWidget")
        self.SD = QtWidgets.QWidget()
        self.SD.setObjectName("SD")
        self.layoutWidget = QtWidgets.QWidget(self.SD)
        self.layoutWidget.setGeometry(QtCore.QRect(650, 20, 111, 231))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ScanSD = QtWidgets.QPushButton(self.layoutWidget)
        self.ScanSD.setMaximumSize(QtCore.QSize(100, 100))
        self.ScanSD.setObjectName("ScanSD")
        self.verticalLayout.addWidget(self.ScanSD)
        self.StartPrint = QtWidgets.QPushButton(self.layoutWidget)
        self.StartPrint.setMaximumSize(QtCore.QSize(100, 100))
        self.StartPrint.setObjectName("StartPrint")
        self.verticalLayout.addWidget(self.StartPrint)
        self.FileList = QtWidgets.QTableWidget(self.SD)
        self.FileList.setGeometry(QtCore.QRect(60, 20, 571, 231))
        self.FileList.setObjectName("FileList")
        self.FileList.setColumnCount(2)
        self.FileList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.FileList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.FileList.setHorizontalHeaderItem(1, item)
        self.tabWidget.addTab(self.SD, "")
        self.USB = QtWidgets.QWidget()
        self.USB.setObjectName("USB")
        self.tabWidget.addTab(self.USB, "")
        self.ActivePrint = QtWidgets.QPushButton(PrintWindow)
        self.ActivePrint.setGeometry(QtCore.QRect(650, 360, 100, 91))
        self.ActivePrint.setMaximumSize(QtCore.QSize(100, 100))
        self.ActivePrint.setObjectName("ActivePrint")

        self.retranslateUi(PrintWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PrintWindow)

    def retranslateUi(self, PrintWindow):
        _translate = QtCore.QCoreApplication.translate
        PrintWindow.setWindowTitle(_translate("PrintWindow", "ControlWindow"))
        self.ScanSD.setText(_translate("PrintWindow", "Scan SD"))
        self.StartPrint.setText(_translate("PrintWindow", "Start Print"))
        item = self.FileList.horizontalHeaderItem(0)
        item.setText(_translate("PrintWindow", "Name"))
        item = self.FileList.horizontalHeaderItem(1)
        item.setText(_translate("PrintWindow", "Size"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SD), _translate("PrintWindow", "SD"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.USB), _translate("PrintWindow", "USB"))
        self.ActivePrint.setText(_translate("PrintWindow", "Active Print"))

