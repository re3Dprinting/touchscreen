# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home_qt.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Home(object):
    def setupUi(self, Home):
        Home.setObjectName("Home")
        Home.resize(800, 448)
        Home.setMinimumSize(QtCore.QSize(800, 448))
        Home.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Home.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Home)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_3 = QtWidgets.QWidget(Home)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Title = QtWidgets.QLabel(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Title.sizePolicy().hasHeightForWidth())
        self.Title.setSizePolicy(sizePolicy)
        self.Title.setObjectName("Title")
        self.horizontalLayout_2.addWidget(self.Title)
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.horizontalLayout_2.addItem(spacerItem)
        self.re3DIcon = QtWidgets.QPushButton(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.re3DIcon.sizePolicy().hasHeightForWidth())
        self.re3DIcon.setSizePolicy(sizePolicy)
        self.re3DIcon.setMinimumSize(QtCore.QSize(0, 0))
        self.re3DIcon.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.re3DIcon.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.re3DIcon.setIcon(icon)
        self.re3DIcon.setIconSize(QtCore.QSize(100, 100))
        self.re3DIcon.setObjectName("re3DIcon")
        self.horizontalLayout_2.addWidget(self.re3DIcon)
        self.verticalLayout.addWidget(self.widget_3)
        self.widget_2 = QtWidgets.QWidget(Home)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushbutton_print = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_print.sizePolicy().hasHeightForWidth())
        self.pushbutton_print.setSizePolicy(sizePolicy)
        self.pushbutton_print.setMinimumSize(QtCore.QSize(150, 150))
        self.pushbutton_print.setMaximumSize(QtCore.QSize(150, 300))
        self.pushbutton_print.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/img/Printing.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_print.setIcon(icon1)
        self.pushbutton_print.setIconSize(QtCore.QSize(150, 150))
        self.pushbutton_print.setObjectName("pushbutton_print")
        self.horizontalLayout_4.addWidget(self.pushbutton_print)
        self.pushbutton_control = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_control.sizePolicy().hasHeightForWidth())
        self.pushbutton_control.setSizePolicy(sizePolicy)
        self.pushbutton_control.setMinimumSize(QtCore.QSize(150, 150))
        self.pushbutton_control.setMaximumSize(QtCore.QSize(150, 300))
        self.pushbutton_control.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/img/Movement.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_control.setIcon(icon2)
        self.pushbutton_control.setIconSize(QtCore.QSize(150, 150))
        self.pushbutton_control.setObjectName("pushbutton_control")
        self.horizontalLayout_4.addWidget(self.pushbutton_control)
        self.pushbutton_temperature = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_temperature.sizePolicy().hasHeightForWidth())
        self.pushbutton_temperature.setSizePolicy(sizePolicy)
        self.pushbutton_temperature.setMinimumSize(QtCore.QSize(150, 150))
        self.pushbutton_temperature.setMaximumSize(QtCore.QSize(150, 300))
        self.pushbutton_temperature.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/img/img/Temperature_2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_temperature.setIcon(icon3)
        self.pushbutton_temperature.setIconSize(QtCore.QSize(150, 150))
        self.pushbutton_temperature.setObjectName("pushbutton_temperature")
        self.horizontalLayout_4.addWidget(self.pushbutton_temperature)
        self.pushbutton_settings = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushbutton_settings.sizePolicy().hasHeightForWidth())
        self.pushbutton_settings.setSizePolicy(sizePolicy)
        self.pushbutton_settings.setMinimumSize(QtCore.QSize(150, 150))
        self.pushbutton_settings.setMaximumSize(QtCore.QSize(150, 300))
        self.pushbutton_settings.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/img/img/Settings_(2).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushbutton_settings.setIcon(icon4)
        self.pushbutton_settings.setIconSize(QtCore.QSize(150, 150))
        self.pushbutton_settings.setObjectName("pushbutton_settings")
        self.horizontalLayout_4.addWidget(self.pushbutton_settings)
        self.verticalLayout.addWidget(self.widget_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Home)
        QtCore.QMetaObject.connectSlotsByName(Home)

    def retranslateUi(self, Home):
        _translate = QtCore.QCoreApplication.translate
        Home.setWindowTitle(_translate("Home", "TouchDisplay"))
        self.Title.setText(_translate("Home", "<html><head/><body><p><span style=\" font-size:36pt;\">re:3Display</span></p></body></html>"))
import img_rc
