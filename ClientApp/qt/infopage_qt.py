# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'infopage_qt.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InfoPage(object):
    def setupUi(self, InfoPage):
        InfoPage.setObjectName("InfoPage")
        InfoPage.resize(800, 448)
        InfoPage.setMaximumSize(QtCore.QSize(800, 448))
        self.Back = QtWidgets.QPushButton(InfoPage)
        self.Back.setGeometry(QtCore.QRect(4, 346, 91, 91))
        self.Back.setMaximumSize(QtCore.QSize(100, 100))
        self.Back.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon)
        self.Back.setIconSize(QtCore.QSize(100, 100))
        self.Back.setObjectName("Back")
        self.w_message_text = QtWidgets.QTextEdit(InfoPage)
        self.w_message_text.setGeometry(QtCore.QRect(160, 30, 580, 360))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_message_text.sizePolicy().hasHeightForWidth())
        self.w_message_text.setSizePolicy(sizePolicy)
        self.w_message_text.setMaximumSize(QtCore.QSize(115200, 1000))
        self.w_message_text.setObjectName("w_message_text")
        self.widget = QtWidgets.QWidget(InfoPage)
        self.widget.setGeometry(QtCore.QRect(40, 30, 112, 286))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.w_pushbutton_info = QtWidgets.QPushButton(self.widget)
        self.w_pushbutton_info.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_info.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_pushbutton_info.setObjectName("w_pushbutton_info")
        self.verticalLayout_2.addWidget(self.w_pushbutton_info)
        self.w_pushbutton_capabilities = QtWidgets.QPushButton(self.widget)
        self.w_pushbutton_capabilities.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_capabilities.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_pushbutton_capabilities.setObjectName("w_pushbutton_capabilities")
        self.verticalLayout_2.addWidget(self.w_pushbutton_capabilities)
        self.w_pushbutton_stats = QtWidgets.QPushButton(self.widget)
        self.w_pushbutton_stats.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_stats.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_pushbutton_stats.setObjectName("w_pushbutton_stats")
        self.verticalLayout_2.addWidget(self.w_pushbutton_stats)
        self.w_pushbutton_settings = QtWidgets.QPushButton(self.widget)
        self.w_pushbutton_settings.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_settings.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_pushbutton_settings.setObjectName("w_pushbutton_settings")
        self.verticalLayout_2.addWidget(self.w_pushbutton_settings)

        self.retranslateUi(InfoPage)
        QtCore.QMetaObject.connectSlotsByName(InfoPage)

    def retranslateUi(self, InfoPage):
        _translate = QtCore.QCoreApplication.translate
        InfoPage.setWindowTitle(_translate("InfoPage", "ControlWindow"))
        self.w_pushbutton_info.setText(_translate("InfoPage", "Printer Info"))
        self.w_pushbutton_capabilities.setText(_translate("InfoPage", "Printer\n"
"Capabilities"))
        self.w_pushbutton_stats.setText(_translate("InfoPage", "Printer Stats"))
        self.w_pushbutton_settings.setText(_translate("InfoPage", "Printer\n"
"Settings"))
import img_rc
