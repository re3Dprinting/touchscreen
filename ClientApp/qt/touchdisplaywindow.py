# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/touchdisplay.ui',
# licensing of 'qt/touchdisplay.ui' applies.
#
# Created: Fri Aug  2 14:36:56 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_TouchDisplay(object):
    def setupUi(self, TouchDisplay):
        TouchDisplay.setObjectName("TouchDisplay")
        TouchDisplay.resize(641, 326)
        TouchDisplay.setMinimumSize(QtCore.QSize(641, 326))
        TouchDisplay.setMaximumSize(QtCore.QSize(641, 326))
        self.verticalLayout = QtWidgets.QVBoxLayout(TouchDisplay)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(TouchDisplay)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(TouchDisplay)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(TouchDisplay)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(TouchDisplay)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TouchDisplay)
        QtCore.QMetaObject.connectSlotsByName(TouchDisplay)

    def retranslateUi(self, TouchDisplay):
        TouchDisplay.setWindowTitle(QtWidgets.QApplication.translate("TouchDisplay", "Form", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("TouchDisplay", "Hello World", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("TouchDisplay", "Does This", None, -1))
        self.pushButton_3.setText(QtWidgets.QApplication.translate("TouchDisplay", "Work?", None, -1))

