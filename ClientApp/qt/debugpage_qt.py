# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'debugpage_qt.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DebugPage(object):
    def setupUi(self, DebugPage):
        DebugPage.setObjectName("DebugPage")
        DebugPage.resize(800, 448)
        DebugPage.setMaximumSize(QtCore.QSize(800, 448))
        self.Back = QtWidgets.QPushButton(DebugPage)
        self.Back.setGeometry(QtCore.QRect(4, 346, 91, 91))
        self.Back.setMaximumSize(QtCore.QSize(100, 100))
        self.Back.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon)
        self.Back.setIconSize(QtCore.QSize(100, 100))
        self.Back.setObjectName("Back")
        self.w_message_text = QtWidgets.QTextBrowser(DebugPage)
        self.w_message_text.setGeometry(QtCore.QRect(160, 80, 580, 291))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_message_text.sizePolicy().hasHeightForWidth())
        self.w_message_text.setSizePolicy(sizePolicy)
        self.w_message_text.setMaximumSize(QtCore.QSize(115200, 1000))
        self.w_message_text.setObjectName("w_message_text")
        self.w_lineedit_message = QtWidgets.QLineEdit(DebugPage)
        self.w_lineedit_message.setGeometry(QtCore.QRect(160, 30, 580, 41))
        self.w_lineedit_message.setObjectName("w_lineedit_message")
        self.horizontalLayoutWidget = QtWidgets.QWidget(DebugPage)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(160, 380, 181, 41))
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
        self.widget = QtWidgets.QWidget(DebugPage)
        self.widget.setGeometry(QtCore.QRect(40, 30, 112, 214))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.w_pushbutton_add_marker = QtWidgets.QPushButton(self.widget)
        self.w_pushbutton_add_marker.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_add_marker.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_pushbutton_add_marker.setObjectName("w_pushbutton_add_marker")
        self.verticalLayout_2.addWidget(self.w_pushbutton_add_marker)
        self.w_pushbutton_copy_log = QtWidgets.QPushButton(self.widget)
        self.w_pushbutton_copy_log.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_copy_log.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_pushbutton_copy_log.setObjectName("w_pushbutton_copy_log")
        self.verticalLayout_2.addWidget(self.w_pushbutton_copy_log)
        self.w_pushbutton_send_fake_ack = QtWidgets.QPushButton(self.widget)
        self.w_pushbutton_send_fake_ack.setMaximumSize(QtCore.QSize(100, 100))
        self.w_pushbutton_send_fake_ack.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_pushbutton_send_fake_ack.setObjectName("w_pushbutton_send_fake_ack")
        self.verticalLayout_2.addWidget(self.w_pushbutton_send_fake_ack)

        self.retranslateUi(DebugPage)
        QtCore.QMetaObject.connectSlotsByName(DebugPage)

    def retranslateUi(self, DebugPage):
        _translate = QtCore.QCoreApplication.translate
        DebugPage.setWindowTitle(_translate("DebugPage", "ControlWindow"))
        self.label.setText(_translate("DebugPage", "Logging level:"))
        self.w_combobox_debuglevel.setItemText(0, _translate("DebugPage", "DEBUG"))
        self.w_combobox_debuglevel.setItemText(1, _translate("DebugPage", "INFO"))
        self.w_pushbutton_add_marker.setText(_translate("DebugPage", "Add Log\n"
"Marker"))
        self.w_pushbutton_copy_log.setText(_translate("DebugPage", "Copy Log\n"
"Files"))
        self.w_pushbutton_send_fake_ack.setText(_translate("DebugPage", "Send Fake\n"
"ACK"))
