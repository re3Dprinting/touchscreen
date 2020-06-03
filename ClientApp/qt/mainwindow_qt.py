# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow_qt.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setStyleSheet("")
        self.stack = QtWidgets.QStackedWidget(MainWindow)
        self.stack.setGeometry(QtCore.QRect(0, 0, 800, 448))
        self.stack.setObjectName("stack")
        self.stackedWidgetPage1 = QtWidgets.QWidget()
        self.stackedWidgetPage1.setObjectName("stackedWidgetPage1")
        self.stack.addWidget(self.stackedWidgetPage1)
        self.status = QtWidgets.QWidget(MainWindow)
        self.status.setGeometry(QtCore.QRect(0, 448, 800, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        self.status.setStyleSheet("QWidget { border-top: 1px solid #ccc; }")
        self.status.setObjectName("status")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.status)
        self.horizontalLayout.setContentsMargins(12, 0, 12, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left_status = QtWidgets.QLabel(self.status)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.left_status.setFont(font)
        self.left_status.setText("")
        self.left_status.setObjectName("left_status")
        self.horizontalLayout.addWidget(self.left_status)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.middle_status = QtWidgets.QLabel(self.status)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.middle_status.setFont(font)
        self.middle_status.setText("")
        self.middle_status.setObjectName("middle_status")
        self.horizontalLayout.addWidget(self.middle_status)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.right_status = QtWidgets.QLabel(self.status)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.right_status.setFont(font)
        self.right_status.setText("")
        self.right_status.setObjectName("right_status")
        self.horizontalLayout.addWidget(self.right_status)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Form"))
import img_rc
