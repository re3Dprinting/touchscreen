# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userupdatepage_qt.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UserUpdatePage(object):
    def setupUi(self, UserUpdatePage):
        UserUpdatePage.setObjectName("UserUpdatePage")
        UserUpdatePage.resize(800, 448)
        UserUpdatePage.setMaximumSize(QtCore.QSize(800, 448))
        self.CurrentVersion = QtWidgets.QLabel(UserUpdatePage)
        self.CurrentVersion.setGeometry(QtCore.QRect(40, 12, 97, 16))
        self.CurrentVersion.setObjectName("CurrentVersion")
        self.widget = QtWidgets.QWidget(UserUpdatePage)
        self.widget.setGeometry(QtCore.QRect(40, 40, 112, 142))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.CheckUpdate = QtWidgets.QPushButton(self.widget)
        self.CheckUpdate.setMaximumSize(QtCore.QSize(150, 100))
        self.CheckUpdate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.CheckUpdate.setObjectName("CheckUpdate")
        self.verticalLayout_2.addWidget(self.CheckUpdate)
        self.Update = QtWidgets.QPushButton(self.widget)
        self.Update.setMaximumSize(QtCore.QSize(150, 100))
        self.Update.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Update.setObjectName("Update")
        self.verticalLayout_2.addWidget(self.Update)
        self.widget_2 = QtWidgets.QWidget(UserUpdatePage)
        self.widget_2.setGeometry(QtCore.QRect(160, 40, 580, 360))
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SoftwareList = QtWidgets.QTableWidget(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SoftwareList.sizePolicy().hasHeightForWidth())
        self.SoftwareList.setSizePolicy(sizePolicy)
        self.SoftwareList.setObjectName("SoftwareList")
        self.SoftwareList.setColumnCount(2)
        self.SoftwareList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.SoftwareList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.SoftwareList.setHorizontalHeaderItem(1, item)
        self.horizontalLayout.addWidget(self.SoftwareList)
        self.DebugOutput = QtWidgets.QTextBrowser(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DebugOutput.sizePolicy().hasHeightForWidth())
        self.DebugOutput.setSizePolicy(sizePolicy)
        self.DebugOutput.setMaximumSize(QtCore.QSize(400, 16777215))
        self.DebugOutput.setObjectName("DebugOutput")
        self.horizontalLayout.addWidget(self.DebugOutput)
        self.Back = QtWidgets.QPushButton(UserUpdatePage)
        self.Back.setGeometry(QtCore.QRect(5, 347, 90, 90))
        self.Back.setMaximumSize(QtCore.QSize(100, 100))
        self.Back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon)
        self.Back.setIconSize(QtCore.QSize(100, 100))
        self.Back.setObjectName("Back")

        self.retranslateUi(UserUpdatePage)
        QtCore.QMetaObject.connectSlotsByName(UserUpdatePage)

    def retranslateUi(self, UserUpdatePage):
        _translate = QtCore.QCoreApplication.translate
        UserUpdatePage.setWindowTitle(_translate("UserUpdatePage", "ControlWindow"))
        self.CurrentVersion.setText(_translate("UserUpdatePage", "Current Version:"))
        self.CheckUpdate.setText(_translate("UserUpdatePage", "Check for\n"
"Update"))
        self.Update.setText(_translate("UserUpdatePage", "Update/\n"
"Rollback"))
        item = self.SoftwareList.horizontalHeaderItem(0)
        item.setText(_translate("UserUpdatePage", "Version"))
        item = self.SoftwareList.horizontalHeaderItem(1)
        item.setText(_translate("UserUpdatePage", "Release Time"))
