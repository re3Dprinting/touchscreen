# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'printpage_qt.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PrintPage(object):
    def setupUi(self, PrintPage):
        PrintPage.setObjectName("PrintPage")
        PrintPage.resize(800, 448)
        PrintPage.setMaximumSize(QtCore.QSize(800, 448))
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(PrintPage)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LeftBar = QtWidgets.QWidget(PrintPage)
        self.LeftBar.setObjectName("LeftBar")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.LeftBar)
        self.verticalLayout_6.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushbutton_SDtab = QtWidgets.QPushButton(self.LeftBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_SDtab.sizePolicy().hasHeightForWidth())
        self.pushbutton_SDtab.setSizePolicy(sizePolicy)
        self.pushbutton_SDtab.setMinimumSize(QtCore.QSize(160, 60))
        self.pushbutton_SDtab.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushbutton_SDtab.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/SD.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_SDtab.setIcon(icon)
        self.pushbutton_SDtab.setIconSize(QtCore.QSize(160, 40))
        self.pushbutton_SDtab.setObjectName("pushbutton_SDtab")
        self.verticalLayout_6.addWidget(self.pushbutton_SDtab)
        self.pushbutton_USBtab = QtWidgets.QPushButton(self.LeftBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_USBtab.sizePolicy().hasHeightForWidth())
        self.pushbutton_USBtab.setSizePolicy(sizePolicy)
        self.pushbutton_USBtab.setMinimumSize(QtCore.QSize(160, 60))
        self.pushbutton_USBtab.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushbutton_USBtab.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/img/USB_(2).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_USBtab.setIcon(icon1)
        self.pushbutton_USBtab.setIconSize(QtCore.QSize(160, 40))
        self.pushbutton_USBtab.setObjectName("pushbutton_USBtab")
        self.verticalLayout_6.addWidget(self.pushbutton_USBtab)
        self.pushbutton_Localtab = QtWidgets.QPushButton(self.LeftBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_Localtab.sizePolicy().hasHeightForWidth())
        self.pushbutton_Localtab.setSizePolicy(sizePolicy)
        self.pushbutton_Localtab.setMinimumSize(QtCore.QSize(160, 60))
        self.pushbutton_Localtab.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushbutton_Localtab.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/img/LOCAL.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_Localtab.setIcon(icon2)
        self.pushbutton_Localtab.setIconSize(QtCore.QSize(160, 40))
        self.pushbutton_Localtab.setObjectName("pushbutton_Localtab")
        self.verticalLayout_6.addWidget(self.pushbutton_Localtab)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_6.addItem(spacerItem1)
        self.pushbutton_folder_up = QtWidgets.QPushButton(self.LeftBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_folder_up.sizePolicy().hasHeightForWidth())
        self.pushbutton_folder_up.setSizePolicy(sizePolicy)
        self.pushbutton_folder_up.setMinimumSize(QtCore.QSize(160, 50))
        self.pushbutton_folder_up.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushbutton_folder_up.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/img/img/Up_one_folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_folder_up.setIcon(icon3)
        self.pushbutton_folder_up.setIconSize(QtCore.QSize(160, 40))
        self.pushbutton_folder_up.setObjectName("pushbutton_folder_up")
        self.verticalLayout_6.addWidget(self.pushbutton_folder_up)
        self.pushbutton_folder_open = QtWidgets.QPushButton(self.LeftBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_folder_open.sizePolicy().hasHeightForWidth())
        self.pushbutton_folder_open.setSizePolicy(sizePolicy)
        self.pushbutton_folder_open.setMinimumSize(QtCore.QSize(160, 50))
        self.pushbutton_folder_open.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushbutton_folder_open.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/img/img/Open_folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_folder_open.setIcon(icon4)
        self.pushbutton_folder_open.setIconSize(QtCore.QSize(160, 40))
        self.pushbutton_folder_open.setObjectName("pushbutton_folder_open")
        self.verticalLayout_6.addWidget(self.pushbutton_folder_open)
        self.pushbutton_scan_sd = QtWidgets.QPushButton(self.LeftBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_scan_sd.sizePolicy().hasHeightForWidth())
        self.pushbutton_scan_sd.setSizePolicy(sizePolicy)
        self.pushbutton_scan_sd.setMinimumSize(QtCore.QSize(160, 60))
        self.pushbutton_scan_sd.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushbutton_scan_sd.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/img/img/Scan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_scan_sd.setIcon(icon5)
        self.pushbutton_scan_sd.setIconSize(QtCore.QSize(160, 40))
        self.pushbutton_scan_sd.setObjectName("pushbutton_scan_sd")
        self.verticalLayout_6.addWidget(self.pushbutton_scan_sd)
        self.horizontalLayout.addWidget(self.LeftBar)
        self.stackedPrintingOptions = QtWidgets.QStackedWidget(PrintPage)
        self.stackedPrintingOptions.setObjectName("stackedPrintingOptions")
        self.SD = QtWidgets.QWidget()
        self.SD.setObjectName("SD")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.SD)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sd_pathlabel = QtWidgets.QLabel(self.SD)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sd_pathlabel.setFont(font)
        self.sd_pathlabel.setObjectName("sd_pathlabel")
        self.verticalLayout_2.addWidget(self.sd_pathlabel)
        self.SDFileList = QtWidgets.QTableWidget(self.SD)
        self.SDFileList.setObjectName("SDFileList")
        self.SDFileList.setColumnCount(2)
        self.SDFileList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.SDFileList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.SDFileList.setHorizontalHeaderItem(1, item)
        self.verticalLayout_2.addWidget(self.SDFileList)
        self.stackedPrintingOptions.addWidget(self.SD)
        self.USB = QtWidgets.QWidget()
        self.USB.setObjectName("USB")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.USB)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.usb_pathlabel = QtWidgets.QLabel(self.USB)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.usb_pathlabel.setFont(font)
        self.usb_pathlabel.setObjectName("usb_pathlabel")
        self.verticalLayout_3.addWidget(self.usb_pathlabel)
        self.USBFileList = QtWidgets.QTableWidget(self.USB)
        self.USBFileList.setObjectName("USBFileList")
        self.USBFileList.setColumnCount(2)
        self.USBFileList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.USBFileList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.USBFileList.setHorizontalHeaderItem(1, item)
        self.verticalLayout_3.addWidget(self.USBFileList)
        self.stackedPrintingOptions.addWidget(self.USB)
        self.Local = QtWidgets.QWidget()
        self.Local.setObjectName("Local")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Local)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.loc_pathlabel = QtWidgets.QLabel(self.Local)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.loc_pathlabel.setFont(font)
        self.loc_pathlabel.setObjectName("loc_pathlabel")
        self.verticalLayout_4.addWidget(self.loc_pathlabel)
        self.LocalFileList = QtWidgets.QTableWidget(self.Local)
        self.LocalFileList.setObjectName("LocalFileList")
        self.LocalFileList.setColumnCount(2)
        self.LocalFileList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.LocalFileList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.LocalFileList.setHorizontalHeaderItem(1, item)
        self.verticalLayout_4.addWidget(self.LocalFileList)
        self.stackedPrintingOptions.addWidget(self.Local)
        self.horizontalLayout.addWidget(self.stackedPrintingOptions)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.BottomBar = QtWidgets.QWidget(PrintPage)
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
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/img/img/Small_arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon6)
        self.Back.setIconSize(QtCore.QSize(55, 55))
        self.Back.setObjectName("Back")
        self.horizontalLayout_2.addWidget(self.Back)
        spacerItem2 = QtWidgets.QSpacerItem(282, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushbutton_stop_print = QtWidgets.QPushButton(self.BottomBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_stop_print.sizePolicy().hasHeightForWidth())
        self.pushbutton_stop_print.setSizePolicy(sizePolicy)
        self.pushbutton_stop_print.setMinimumSize(QtCore.QSize(0, 0))
        self.pushbutton_stop_print.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushbutton_stop_print.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/img/img/USB.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_stop_print.setIcon(icon7)
        self.pushbutton_stop_print.setIconSize(QtCore.QSize(120, 60))
        self.pushbutton_stop_print.setObjectName("pushbutton_stop_print")
        self.horizontalLayout_2.addWidget(self.pushbutton_stop_print)
        self.pushbutton_start_print = QtWidgets.QPushButton(self.BottomBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_start_print.sizePolicy().hasHeightForWidth())
        self.pushbutton_start_print.setSizePolicy(sizePolicy)
        self.pushbutton_start_print.setMinimumSize(QtCore.QSize(0, 0))
        self.pushbutton_start_print.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushbutton_start_print.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/img/img/Start_Print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_start_print.setIcon(icon8)
        self.pushbutton_start_print.setIconSize(QtCore.QSize(120, 60))
        self.pushbutton_start_print.setObjectName("pushbutton_start_print")
        self.horizontalLayout_2.addWidget(self.pushbutton_start_print)
        self.pushbutton_active_print = QtWidgets.QPushButton(self.BottomBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_active_print.sizePolicy().hasHeightForWidth())
        self.pushbutton_active_print.setSizePolicy(sizePolicy)
        self.pushbutton_active_print.setMinimumSize(QtCore.QSize(0, 0))
        self.pushbutton_active_print.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushbutton_active_print.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/img/img/Active_Print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_active_print.setIcon(icon9)
        self.pushbutton_active_print.setIconSize(QtCore.QSize(120, 60))
        self.pushbutton_active_print.setObjectName("pushbutton_active_print")
        self.horizontalLayout_2.addWidget(self.pushbutton_active_print)
        self.verticalLayout_7.addWidget(self.BottomBar)

        self.retranslateUi(PrintPage)
        self.stackedPrintingOptions.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PrintPage)

    def retranslateUi(self, PrintPage):
        _translate = QtCore.QCoreApplication.translate
        PrintPage.setWindowTitle(_translate("PrintPage", "ControlWindow"))
        self.sd_pathlabel.setText(_translate("PrintPage", "Files on Viki SD Card"))
        item = self.SDFileList.horizontalHeaderItem(0)
        item.setText(_translate("PrintPage", "Name"))
        item = self.SDFileList.horizontalHeaderItem(1)
        item.setText(_translate("PrintPage", "Size"))
        self.usb_pathlabel.setText(_translate("PrintPage", "TextLabel"))
        item = self.USBFileList.horizontalHeaderItem(0)
        item.setText(_translate("PrintPage", "Name"))
        item = self.USBFileList.horizontalHeaderItem(1)
        item.setText(_translate("PrintPage", "Size"))
        self.loc_pathlabel.setText(_translate("PrintPage", "TextLabel"))
        item = self.LocalFileList.horizontalHeaderItem(0)
        item.setText(_translate("PrintPage", "Name"))
        item = self.LocalFileList.horizontalHeaderItem(1)
        item.setText(_translate("PrintPage", "Size"))
import img_rc
