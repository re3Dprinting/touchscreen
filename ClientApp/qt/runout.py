# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/runout.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_w_runout_dialog(object):
    def setupUi(self, w_runout_dialog):
        w_runout_dialog.setObjectName("w_runout_dialog")
        w_runout_dialog.resize(344, 188)
        w_runout_dialog.setModal(True)
        self.w_buttonBox = QtWidgets.QDialogButtonBox(w_runout_dialog)
        self.w_buttonBox.setGeometry(QtCore.QRect(30, 140, 291, 32))
        self.w_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.w_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.w_buttonBox.setObjectName("w_buttonBox")
        self.w_runout_title = QtWidgets.QLabel(w_runout_dialog)
        self.w_runout_title.setGeometry(QtCore.QRect(50, 10, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.w_runout_title.setFont(font)
        self.w_runout_title.setAlignment(QtCore.Qt.AlignCenter)
        self.w_runout_title.setWordWrap(True)
        self.w_runout_title.setObjectName("w_runout_title")
        self.w_runout_message_label = QtWidgets.QLabel(w_runout_dialog)
        self.w_runout_message_label.setGeometry(QtCore.QRect(30, 60, 291, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.w_runout_message_label.setFont(font)
        self.w_runout_message_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.w_runout_message_label.setWordWrap(True)
        self.w_runout_message_label.setObjectName("w_runout_message_label")

        self.retranslateUi(w_runout_dialog)
        self.w_buttonBox.accepted.connect(w_runout_dialog.accept)
        self.w_buttonBox.rejected.connect(w_runout_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(w_runout_dialog)

    def retranslateUi(self, w_runout_dialog):
        _translate = QtCore.QCoreApplication.translate
        w_runout_dialog.setWindowTitle(_translate("w_runout_dialog", "Dialog"))
        self.w_runout_title.setText(_translate("w_runout_dialog", "Filament Change"))
        self.w_runout_message_label.setText(_translate("w_runout_dialog", "Filament change instructions"))
