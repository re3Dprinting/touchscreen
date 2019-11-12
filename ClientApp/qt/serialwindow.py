# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/serialwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from builtins import object
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
        self.widget = QtWidgets.QWidget(SerialWindow)
        self.widget.setGeometry(QtCore.QRect(50, 70, 711, 261))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ScanSerial = QtWidgets.QPushButton(self.widget)
        self.ScanSerial.setMaximumSize(QtCore.QSize(100, 100))
        self.ScanSerial.setObjectName("ScanSerial")
        self.verticalLayout.addWidget(self.ScanSerial)
        self.ConnectSerial = QtWidgets.QPushButton(self.widget)
        self.ConnectSerial.setMaximumSize(QtCore.QSize(100, 100))
        self.ConnectSerial.setObjectName("ConnectSerial")
        self.verticalLayout.addWidget(self.ConnectSerial)
        self.DisconnectSerial = QtWidgets.QPushButton(self.widget)
        self.DisconnectSerial.setMaximumSize(QtCore.QSize(100, 100))
        self.DisconnectSerial.setObjectName("DisconnectSerial")
        self.verticalLayout.addWidget(self.DisconnectSerial)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.COMlist = QtWidgets.QTableWidget(self.widget)
        self.COMlist.setObjectName("COMlist")
        self.COMlist.setColumnCount(2)
        self.COMlist.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.COMlist.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.COMlist.setHorizontalHeaderItem(1, item)
        self.horizontalLayout_4.addWidget(self.COMlist)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        self.SerialOutput = QtWidgets.QTextBrowser(self.widget)
        self.SerialOutput.setObjectName("SerialOutput")
        self.horizontalLayout.addWidget(self.SerialOutput)

        self.retranslateUi(SerialWindow)
        QtCore.QMetaObject.connectSlotsByName(SerialWindow)

    def retranslateUi(self, SerialWindow):
        _translate = QtCore.QCoreApplication.translate
        SerialWindow.setWindowTitle(_translate("SerialWindow", "ControlWindow"))
        self.ScanSerial.setText(_translate("SerialWindow", "Scan"))
        self.ConnectSerial.setText(_translate("SerialWindow", "Connect"))
        self.DisconnectSerial.setText(_translate("SerialWindow", "Disconnect"))
        item = self.COMlist.horizontalHeaderItem(0)
        item.setText(_translate("SerialWindow", "Device"))
        item = self.COMlist.horizontalHeaderItem(1)
        item.setText(_translate("SerialWindow", "Description"))

