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
        self.verticalLayout = QtWidgets.QVBoxLayout(SerialPage)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.LeftBar = QtWidgets.QWidget(SerialPage)
        self.LeftBar.setObjectName("LeftBar")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.LeftBar)
        self.verticalLayout_7.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.w_pushbutton_scan = QtWidgets.QPushButton(self.LeftBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_scan.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_scan.setSizePolicy(sizePolicy)
        self.w_pushbutton_scan.setMinimumSize(QtCore.QSize(160, 85))
        self.w_pushbutton_scan.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.w_pushbutton_scan.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/Scan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.w_pushbutton_scan.setIcon(icon)
        self.w_pushbutton_scan.setIconSize(QtCore.QSize(160, 40))
        self.w_pushbutton_scan.setObjectName("w_pushbutton_scan")
        self.verticalLayout_7.addWidget(self.w_pushbutton_scan)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_7.addItem(spacerItem1)
        self.horizontalLayout_3.addWidget(self.LeftBar)
        self.frame = QtWidgets.QFrame(SerialPage)
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
        self.horizontalLayout_3.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.BottomBar = QtWidgets.QWidget(SerialPage)
        self.BottomBar.setObjectName("BottomBar")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.BottomBar)
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Back = QtWidgets.QPushButton(self.BottomBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Back.sizePolicy().hasHeightForWidth())
        self.Back.setSizePolicy(sizePolicy)
        self.Back.setMinimumSize(QtCore.QSize(65, 65))
        self.Back.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.Back.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Back.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/img/Small_arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon1)
        self.Back.setIconSize(QtCore.QSize(55, 55))
        self.Back.setObjectName("Back")
        self.horizontalLayout_2.addWidget(self.Back)
        spacerItem2 = QtWidgets.QSpacerItem(282, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.w_pushbutton_disconnect = QtWidgets.QPushButton(self.BottomBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_disconnect.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_disconnect.setSizePolicy(sizePolicy)
        self.w_pushbutton_disconnect.setMinimumSize(QtCore.QSize(0, 0))
        self.w_pushbutton_disconnect.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.w_pushbutton_disconnect.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/img/Disconnect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.w_pushbutton_disconnect.setIcon(icon2)
        self.w_pushbutton_disconnect.setIconSize(QtCore.QSize(120, 60))
        self.w_pushbutton_disconnect.setObjectName("w_pushbutton_disconnect")
        self.horizontalLayout_2.addWidget(self.w_pushbutton_disconnect)
        self.w_pushbutton_connect = QtWidgets.QPushButton(self.BottomBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_connect.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_connect.setSizePolicy(sizePolicy)
        self.w_pushbutton_connect.setMinimumSize(QtCore.QSize(0, 0))
        self.w_pushbutton_connect.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.w_pushbutton_connect.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/img/img/Connect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.w_pushbutton_connect.setIcon(icon3)
        self.w_pushbutton_connect.setIconSize(QtCore.QSize(120, 40))
        self.w_pushbutton_connect.setObjectName("w_pushbutton_connect")
        self.horizontalLayout_2.addWidget(self.w_pushbutton_connect)
        self.verticalLayout.addWidget(self.BottomBar)

        self.retranslateUi(SerialPage)
        QtCore.QMetaObject.connectSlotsByName(SerialPage)

    def retranslateUi(self, SerialPage):
        _translate = QtCore.QCoreApplication.translate
        SerialPage.setWindowTitle(_translate("SerialPage", "ControlWindow"))
        item = self.w_table_ports.horizontalHeaderItem(0)
        item.setText(_translate("SerialPage", "Device"))
import img_rc
