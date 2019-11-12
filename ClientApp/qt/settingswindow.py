# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/settingswindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(800, 480)
        SettingsWindow.setMinimumSize(QtCore.QSize(800, 480))
        SettingsWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingsWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Server = QtWidgets.QPushButton(SettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Server.sizePolicy().hasHeightForWidth())
        self.Server.setSizePolicy(sizePolicy)
        self.Server.setMinimumSize(QtCore.QSize(150, 350))
        self.Server.setMaximumSize(QtCore.QSize(150, 16777215))
        self.Server.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/server.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Server.setIcon(icon)
        self.Server.setIconSize(QtCore.QSize(150, 150))
        self.Server.setObjectName("Server")
        self.horizontalLayout_2.addWidget(self.Server)
        self.Serial = QtWidgets.QPushButton(SettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Serial.sizePolicy().hasHeightForWidth())
        self.Serial.setSizePolicy(sizePolicy)
        self.Serial.setMinimumSize(QtCore.QSize(150, 350))
        self.Serial.setMaximumSize(QtCore.QSize(150, 16777215))
        self.Serial.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/serial.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Serial.setIcon(icon1)
        self.Serial.setIconSize(QtCore.QSize(150, 150))
        self.Serial.setObjectName("Serial")
        self.horizontalLayout_2.addWidget(self.Serial)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Back = QtWidgets.QPushButton(SettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Back.sizePolicy().hasHeightForWidth())
        self.Back.setSizePolicy(sizePolicy)
        self.Back.setMinimumSize(QtCore.QSize(100, 100))
        self.Back.setMaximumSize(QtCore.QSize(100, 100))
        self.Back.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon2)
        self.Back.setIconSize(QtCore.QSize(100, 100))
        self.Back.setObjectName("Back")
        self.horizontalLayout.addWidget(self.Back)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(SettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 65))
        self.label.setMaximumSize(QtCore.QSize(250, 70))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "TouchDisplay"))
        self.label.setText(_translate("SettingsWindow", "V.1.0.0 re3Display"))

