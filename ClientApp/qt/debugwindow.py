# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'debugwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DebugWindow(object):
    def setupUi(self, DebugWindow):
        DebugWindow.setObjectName("DebugWindow")
        DebugWindow.resize(800, 480)
        DebugWindow.setMaximumSize(QtCore.QSize(800, 480))
        self.Back = QtWidgets.QPushButton(DebugWindow)
        self.Back.setGeometry(QtCore.QRect(10, 380, 91, 91))
        self.Back.setMaximumSize(QtCore.QSize(100, 100))
        self.Back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon)
        self.Back.setIconSize(QtCore.QSize(100, 100))
        self.Back.setObjectName("Back")
        self.layoutWidget = QtWidgets.QWidget(DebugWindow)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 111, 281))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.w_pushbutton_add_marker = QtWidgets.QPushButton(self.layoutWidget)
        self.w_pushbutton_add_marker.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_add_marker.setObjectName("w_pushbutton_add_marker")
        self.verticalLayout.addWidget(self.w_pushbutton_add_marker)
        self.w_pushbutton_copy_log = QtWidgets.QPushButton(self.layoutWidget)
        self.w_pushbutton_copy_log.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_copy_log.setObjectName("w_pushbutton_copy_log")
        self.verticalLayout.addWidget(self.w_pushbutton_copy_log)
        self.w_pushbutton_send_fake_ack = QtWidgets.QPushButton(self.layoutWidget)
        self.w_pushbutton_send_fake_ack.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_send_fake_ack.setObjectName("w_pushbutton_send_fake_ack")
        self.verticalLayout.addWidget(self.w_pushbutton_send_fake_ack)
        self.w_message_text = QtWidgets.QTextBrowser(DebugWindow)
        self.w_message_text.setGeometry(QtCore.QRect(140, 80, 601, 311))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_message_text.sizePolicy().hasHeightForWidth())
        self.w_message_text.setSizePolicy(sizePolicy)
        self.w_message_text.setMaximumSize(QtCore.QSize(115200, 1000))
        self.w_message_text.setObjectName("w_message_text")
        self.w_lineedit_message = QtWidgets.QLineEdit(DebugWindow)
        self.w_lineedit_message.setGeometry(QtCore.QRect(140, 30, 601, 41))
        self.w_lineedit_message.setObjectName("w_lineedit_message")
        self.horizontalLayoutWidget = QtWidgets.QWidget(DebugWindow)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(140, 410, 181, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.w_combobox_debuglevel = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.w_combobox_debuglevel.setObjectName("w_combobox_debuglevel")
        self.w_combobox_debuglevel.addItem("")
        self.w_combobox_debuglevel.addItem("")
        self.horizontalLayout.addWidget(self.w_combobox_debuglevel)

        self.retranslateUi(DebugWindow)
        QtCore.QMetaObject.connectSlotsByName(DebugWindow)

    def retranslateUi(self, DebugWindow):
        _translate = QtCore.QCoreApplication.translate
        DebugWindow.setWindowTitle(_translate("DebugWindow", "ControlWindow"))
        self.w_pushbutton_add_marker.setText(_translate("DebugWindow", "Add Log\n"
"Marker"))
        self.w_pushbutton_copy_log.setText(_translate("DebugWindow", "Copy Log\n"
"Files"))
        self.w_pushbutton_send_fake_ack.setText(_translate("DebugWindow", "Send Fake\n"
"ACK"))
        self.label.setText(_translate("DebugWindow", "Logging level:"))
        self.w_combobox_debuglevel.setItemText(0, _translate("DebugWindow", "DEBUG"))
        self.w_combobox_debuglevel.setItemText(1, _translate("DebugWindow", "INFO"))
