# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serverwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ServerWindow(object):
    def setupUi(self, ServerWindow):
        ServerWindow.setObjectName("ServerWindow")
        ServerWindow.resize(800, 480)
        ServerWindow.setMaximumSize(QtCore.QSize(800, 480))
        self.Back = QtWidgets.QPushButton(ServerWindow)
        self.Back.setGeometry(QtCore.QRect(10, 380, 91, 91))
        self.Back.setMaximumSize(QtCore.QSize(100, 100))
        self.Back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon)
        self.Back.setIconSize(QtCore.QSize(100, 100))
        self.Back.setObjectName("Back")
        self.layoutWidget = QtWidgets.QWidget(ServerWindow)
        self.layoutWidget.setGeometry(QtCore.QRect(90, 90, 131, 271))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Ping = QtWidgets.QPushButton(self.layoutWidget)
        self.Ping.setMaximumSize(QtCore.QSize(100, 100))
        self.Ping.setObjectName("Ping")
        self.verticalLayout.addWidget(self.Ping)
        self.StopPing = QtWidgets.QPushButton(self.layoutWidget)
        self.StopPing.setMaximumSize(QtCore.QSize(100, 100))
        self.StopPing.setObjectName("StopPing")
        self.verticalLayout.addWidget(self.StopPing)
        self.ConnectServer = QtWidgets.QPushButton(self.layoutWidget)
        self.ConnectServer.setMaximumSize(QtCore.QSize(100, 100))
        self.ConnectServer.setObjectName("ConnectServer")
        self.verticalLayout.addWidget(self.ConnectServer)
        self.DisconnectServer = QtWidgets.QPushButton(self.layoutWidget)
        self.DisconnectServer.setMaximumSize(QtCore.QSize(100, 100))
        self.DisconnectServer.setObjectName("DisconnectServer")
        self.verticalLayout.addWidget(self.DisconnectServer)
        self.ServerOutput = QtWidgets.QTextBrowser(ServerWindow)
        self.ServerOutput.setGeometry(QtCore.QRect(240, 90, 500, 281))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ServerOutput.sizePolicy().hasHeightForWidth())
        self.ServerOutput.setSizePolicy(sizePolicy)
        self.ServerOutput.setMaximumSize(QtCore.QSize(500, 1000))
        self.ServerOutput.setObjectName("ServerOutput")
        self.layoutWidget1 = QtWidgets.QWidget(ServerWindow)
        self.layoutWidget1.setGeometry(QtCore.QRect(260, 20, 391, 51))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.IPLabel = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IPLabel.sizePolicy().hasHeightForWidth())
        self.IPLabel.setSizePolicy(sizePolicy)
        self.IPLabel.setObjectName("IPLabel")
        self.horizontalLayout.addWidget(self.IPLabel)
        self.IPText = QtWidgets.QTextEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IPText.sizePolicy().hasHeightForWidth())
        self.IPText.setSizePolicy(sizePolicy)
        self.IPText.setMaximumSize(QtCore.QSize(200, 25))
        self.IPText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.IPText.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.IPText.setObjectName("IPText")
        self.horizontalLayout.addWidget(self.IPText)

        self.retranslateUi(ServerWindow)
        QtCore.QMetaObject.connectSlotsByName(ServerWindow)

    def retranslateUi(self, ServerWindow):
        _translate = QtCore.QCoreApplication.translate
        ServerWindow.setWindowTitle(_translate("ServerWindow", "ControlWindow"))
        self.Ping.setText(_translate("ServerWindow", "Ping"))
        self.StopPing.setText(_translate("ServerWindow", "Stop Ping"))
        self.ConnectServer.setText(_translate("ServerWindow", "Connect"))
        self.DisconnectServer.setText(_translate("ServerWindow", "Disconnect"))
        self.IPLabel.setText(_translate("ServerWindow", "Server IP Address: "))
