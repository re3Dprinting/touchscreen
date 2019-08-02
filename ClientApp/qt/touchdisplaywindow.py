# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/touchdisplaywindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

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
        _translate = QtCore.QCoreApplication.translate
        TouchDisplay.setWindowTitle(_translate("TouchDisplay", "Form"))
        self.pushButton.setText(_translate("TouchDisplay", "Hello World"))
        self.pushButton_2.setText(_translate("TouchDisplay", "Does This"))
        self.pushButton_3.setText(_translate("TouchDisplay", "Work?"))

