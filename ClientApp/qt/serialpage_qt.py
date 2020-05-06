# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serialpage_qt.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SerialPage(object):
    def setupUi(self, SerialPage):
        SerialPage.setObjectName("SerialPage")
        SerialPage.resize(800, 448)
        SerialPage.setMaximumSize(QtCore.QSize(800, 448))
        self.w_pushbutton_back = QtWidgets.QPushButton(SerialPage)
        self.w_pushbutton_back.setGeometry(QtCore.QRect(4, 346, 91, 91))
        self.w_pushbutton_back.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_back.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_pushbutton_back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.w_pushbutton_back.setIcon(icon)
        self.w_pushbutton_back.setIconSize(QtCore.QSize(100, 100))
        self.w_pushbutton_back.setObjectName("w_pushbutton_back")
        self.widget = QtWidgets.QWidget(SerialPage)
        self.widget.setGeometry(QtCore.QRect(40, 30, 112, 214))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.w_pushbutton_scan = QtWidgets.QPushButton(self.widget)
        self.w_pushbutton_scan.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_scan.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_pushbutton_scan.setObjectName("w_pushbutton_scan")
        self.verticalLayout.addWidget(self.w_pushbutton_scan)
        self.w_pushbutton_connect = QtWidgets.QPushButton(self.widget)
        self.w_pushbutton_connect.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_connect.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_pushbutton_connect.setObjectName("w_pushbutton_connect")
        self.verticalLayout.addWidget(self.w_pushbutton_connect)
        self.w_pushbutton_disconnect = QtWidgets.QPushButton(self.widget)
        self.w_pushbutton_disconnect.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_disconnect.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_pushbutton_disconnect.setObjectName("w_pushbutton_disconnect")
        self.verticalLayout.addWidget(self.w_pushbutton_disconnect)
        self.frame = QtWidgets.QFrame(SerialPage)
        self.frame.setGeometry(QtCore.QRect(160, 30, 580, 360))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.w_table_ports = QtWidgets.QTableWidget(self.frame)
        self.w_table_ports.setObjectName("w_table_ports")
        self.w_table_ports.setColumnCount(1)
        self.w_table_ports.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_table_ports.setHorizontalHeaderItem(0, item)
        self.horizontalLayout.addWidget(self.w_table_ports)
        self.w_textb_output = QtWidgets.QTextBrowser(self.frame)
        self.w_textb_output.setObjectName("w_textb_output")
        self.horizontalLayout.addWidget(self.w_textb_output)

        self.retranslateUi(SerialPage)
        QtCore.QMetaObject.connectSlotsByName(SerialPage)

    def retranslateUi(self, SerialPage):
        _translate = QtCore.QCoreApplication.translate
        SerialPage.setWindowTitle(_translate("SerialPage", "ControlWindow"))
        self.w_pushbutton_scan.setText(_translate("SerialPage", "Scan"))
        self.w_pushbutton_connect.setText(_translate("SerialPage", "Connect"))
        self.w_pushbutton_disconnect.setText(_translate("SerialPage", "Disconnect"))
        item = self.w_table_ports.horizontalHeaderItem(0)
        item.setText(_translate("SerialPage", "Device"))
