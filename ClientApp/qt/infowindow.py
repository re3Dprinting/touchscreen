# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'infowindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InfoWindow(object):
    def setupUi(self, InfoWindow):
        InfoWindow.setObjectName("InfoWindow")
        InfoWindow.resize(800, 480)
        InfoWindow.setMaximumSize(QtCore.QSize(800, 480))
        self.Back = QtWidgets.QPushButton(InfoWindow)
        self.Back.setGeometry(QtCore.QRect(10, 380, 91, 91))
        self.Back.setMaximumSize(QtCore.QSize(100, 100))
        self.Back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon)
        self.Back.setIconSize(QtCore.QSize(100, 100))
        self.Back.setObjectName("Back")
        self.layoutWidget = QtWidgets.QWidget(InfoWindow)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 111, 201))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.w_info_button = QtWidgets.QPushButton(self.layoutWidget)
        self.w_info_button.setMaximumSize(QtCore.QSize(100, 100))
        self.w_info_button.setObjectName("w_info_button")
        self.verticalLayout.addWidget(self.w_info_button)
        self.w_stats_button = QtWidgets.QPushButton(self.layoutWidget)
        self.w_stats_button.setMaximumSize(QtCore.QSize(100, 100))
        self.w_stats_button.setObjectName("w_stats_button")
        self.verticalLayout.addWidget(self.w_stats_button)
        self.w_message_text = QtWidgets.QTextBrowser(InfoWindow)
        self.w_message_text.setGeometry(QtCore.QRect(139, 30, 601, 391))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_message_text.sizePolicy().hasHeightForWidth())
        self.w_message_text.setSizePolicy(sizePolicy)
        self.w_message_text.setMaximumSize(QtCore.QSize(115200, 1000))
        self.w_message_text.setObjectName("w_message_text")

        self.retranslateUi(InfoWindow)
        QtCore.QMetaObject.connectSlotsByName(InfoWindow)

    def retranslateUi(self, InfoWindow):
        _translate = QtCore.QCoreApplication.translate
        InfoWindow.setWindowTitle(_translate("InfoWindow", "ControlWindow"))
        self.w_info_button.setText(_translate("InfoWindow", "Printer Info"))
        self.w_stats_button.setText(_translate("InfoWindow", "Printer Stats"))
