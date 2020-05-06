# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notificationwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NotificationWindow(object):
    def setupUi(self, NotificationWindow):
        NotificationWindow.setObjectName("NotificationWindow")
        NotificationWindow.resize(480, 80)
        NotificationWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.horizontalLayout = QtWidgets.QHBoxLayout(NotificationWindow)
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Text = QtWidgets.QLabel(NotificationWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Text.sizePolicy().hasHeightForWidth())
        self.Text.setSizePolicy(sizePolicy)
        self.Text.setAlignment(QtCore.Qt.AlignCenter)
        self.Text.setObjectName("Text")
        self.horizontalLayout.addWidget(self.Text)
        self.Close = QtWidgets.QPushButton(NotificationWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Close.sizePolicy().hasHeightForWidth())
        self.Close.setSizePolicy(sizePolicy)
        self.Close.setMinimumSize(QtCore.QSize(0, 0))
        self.Close.setMaximumSize(QtCore.QSize(50, 50))
        self.Close.setObjectName("Close")
        self.horizontalLayout.addWidget(self.Close)

        self.retranslateUi(NotificationWindow)
        QtCore.QMetaObject.connectSlotsByName(NotificationWindow)

    def retranslateUi(self, NotificationWindow):
        _translate = QtCore.QCoreApplication.translate
        NotificationWindow.setWindowTitle(_translate("NotificationWindow", "Notification"))
        self.Text.setText(_translate("NotificationWindow", "A new Software Version is avalible!"))
        self.Close.setText(_translate("NotificationWindow", "X"))
