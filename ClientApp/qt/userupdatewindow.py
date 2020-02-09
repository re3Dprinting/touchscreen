# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/userupdatewindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UserUpdate(object):
    def setupUi(self, UserUpdate):
        UserUpdate.setObjectName("UserUpdate")
        UserUpdate.resize(800, 480)
        UserUpdate.setMaximumSize(QtCore.QSize(800, 480))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(UserUpdate)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.CurrentVersion = QtWidgets.QLabel(UserUpdate)
        self.CurrentVersion.setObjectName("CurrentVersion")
        self.verticalLayout_2.addWidget(self.CurrentVersion)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.CheckUpdate = QtWidgets.QPushButton(UserUpdate)
        self.CheckUpdate.setMaximumSize(QtCore.QSize(150, 100))
        self.CheckUpdate.setObjectName("CheckUpdate")
        self.verticalLayout.addWidget(self.CheckUpdate)
        self.Update = QtWidgets.QPushButton(UserUpdate)
        self.Update.setMaximumSize(QtCore.QSize(150, 100))
        self.Update.setObjectName("Update")
        self.verticalLayout.addWidget(self.Update)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.SoftwareList = QtWidgets.QTableWidget(UserUpdate)
        self.SoftwareList.setObjectName("SoftwareList")
        self.SoftwareList.setColumnCount(2)
        self.SoftwareList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.SoftwareList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.SoftwareList.setHorizontalHeaderItem(1, item)
        self.horizontalLayout_4.addWidget(self.SoftwareList)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        self.DebugOutput = QtWidgets.QTextBrowser(UserUpdate)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DebugOutput.sizePolicy().hasHeightForWidth())
        self.DebugOutput.setSizePolicy(sizePolicy)
        self.DebugOutput.setMaximumSize(QtCore.QSize(400, 16777215))
        self.DebugOutput.setObjectName("DebugOutput")
        self.horizontalLayout.addWidget(self.DebugOutput)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Back = QtWidgets.QPushButton(UserUpdate)
        self.Back.setMaximumSize(QtCore.QSize(100, 100))
        self.Back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon)
        self.Back.setIconSize(QtCore.QSize(100, 100))
        self.Back.setObjectName("Back")
        self.horizontalLayout_2.addWidget(self.Back)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(UserUpdate)
        QtCore.QMetaObject.connectSlotsByName(UserUpdate)

    def retranslateUi(self, UserUpdate):
        _translate = QtCore.QCoreApplication.translate
        UserUpdate.setWindowTitle(_translate("UserUpdate", "ControlWindow"))
        self.CurrentVersion.setText(_translate("UserUpdate", "Current Version:"))
        self.CheckUpdate.setText(_translate("UserUpdate", "Check for Update"))
        self.Update.setText(_translate("UserUpdate", "Update/Rollback"))
        item = self.SoftwareList.horizontalHeaderItem(0)
        item.setText(_translate("UserUpdate", "Version"))
        item = self.SoftwareList.horizontalHeaderItem(1)
        item.setText(_translate("UserUpdate", "Release Time"))

