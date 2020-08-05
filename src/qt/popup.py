# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popup.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PopUpWindow(object):
    def setupUi(self, PopUpWindow):
        PopUpWindow.setObjectName("PopUpWindow")
        PopUpWindow.resize(400, 240)
        PopUpWindow.setWindowTitle("")
        PopUpWindow.setStyleSheet("")
        PopUpWindow.setModal(False)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(PopUpWindow)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.PopUpMain = QtWidgets.QWidget(PopUpWindow)
        self.PopUpMain.setObjectName("PopUpMain")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.PopUpMain)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.popup_title = QtWidgets.QLabel(self.PopUpMain)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.popup_title.sizePolicy().hasHeightForWidth())
        self.popup_title.setSizePolicy(sizePolicy)
        self.popup_title.setMinimumSize(QtCore.QSize(0, 65))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.popup_title.setFont(font)
        self.popup_title.setTextFormat(QtCore.Qt.PlainText)
        self.popup_title.setAlignment(QtCore.Qt.AlignCenter)
        self.popup_title.setWordWrap(True)
        self.popup_title.setObjectName("popup_title")
        self.verticalLayout.addWidget(self.popup_title)
        self.popup_message = QtWidgets.QLabel(self.PopUpMain)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.popup_message.setFont(font)
        self.popup_message.setAlignment(QtCore.Qt.AlignCenter)
        self.popup_message.setWordWrap(True)
        self.popup_message.setObjectName("popup_message")
        self.verticalLayout.addWidget(self.popup_message)
        self.popup_details = QtWidgets.QLabel(self.PopUpMain)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.popup_details.setFont(font)
        self.popup_details.setText("")
        self.popup_details.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.popup_details.setWordWrap(True)
        self.popup_details.setObjectName("popup_details")
        self.verticalLayout.addWidget(self.popup_details)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.popup_button = QtWidgets.QPushButton(self.PopUpMain)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.popup_button.sizePolicy().hasHeightForWidth())
        self.popup_button.setSizePolicy(sizePolicy)
        self.popup_button.setMinimumSize(QtCore.QSize(100, 0))
        self.popup_button.setIconSize(QtCore.QSize(25, 16))
        self.popup_button.setObjectName("popup_button")
        self.horizontalLayout.addWidget(self.popup_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addWidget(self.PopUpMain)

        self.retranslateUi(PopUpWindow)
        QtCore.QMetaObject.connectSlotsByName(PopUpWindow)

    def retranslateUi(self, PopUpWindow):
        _translate = QtCore.QCoreApplication.translate
        self.popup_title.setText(_translate("PopUpWindow", "Filament Change"))
        self.popup_message.setText(_translate("PopUpWindow", "Filament change instructions\n"
"Line Two"))
        self.popup_button.setText(_translate("PopUpWindow", "OK"))
import img_rc
