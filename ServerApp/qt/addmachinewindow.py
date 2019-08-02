# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/addmachinewindow.ui',
# licensing of 'qt/addmachinewindow.ui' applies.
#
# Created: Fri Aug  2 12:20:44 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_addmachine(object):
    def setupUi(self, addmachine):
        addmachine.setObjectName("addmachine")
        addmachine.resize(470, 240)
        addmachine.setMinimumSize(QtCore.QSize(470, 240))
        addmachine.setMaximumSize(QtCore.QSize(470, 240))
        self.verticalLayout = QtWidgets.QVBoxLayout(addmachine)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Text = QtWidgets.QLabel(addmachine)
        self.Text.setObjectName("Text")
        self.verticalLayout.addWidget(self.Text)
        self.Devices = QtWidgets.QTableWidget(addmachine)
        self.Devices.setObjectName("Devices")
        self.Devices.setColumnCount(3)
        self.Devices.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Devices.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Devices.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Devices.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.Devices)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Refresh = QtWidgets.QPushButton(addmachine)
        self.Refresh.setObjectName("Refresh")
        self.horizontalLayout.addWidget(self.Refresh)
        self.Add = QtWidgets.QPushButton(addmachine)
        self.Add.setObjectName("Add")
        self.horizontalLayout.addWidget(self.Add)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(addmachine)
        QtCore.QMetaObject.connectSlotsByName(addmachine)

    def retranslateUi(self, addmachine):
        addmachine.setWindowTitle(QtWidgets.QApplication.translate("addmachine", "Add Machine", None, -1))
        self.Text.setText(QtWidgets.QApplication.translate("addmachine", "<html><head/><body><p>Please make sure the server is connected and listening for clients.</p><p>Choose a Device to add, and insert the Gigabot Number</p></body></html>", None, -1))
        self.Devices.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("addmachine", "Model", None, -1))
        self.Devices.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("addmachine", "IP Address", None, -1))
        self.Devices.horizontalHeaderItem(2).setText(QtWidgets.QApplication.translate("addmachine", "Gigabot Num", None, -1))
        self.Refresh.setText(QtWidgets.QApplication.translate("addmachine", "Refresh", None, -1))
        self.Add.setText(QtWidgets.QApplication.translate("addmachine", "Add", None, -1))

