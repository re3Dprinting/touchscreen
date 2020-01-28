# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'copy_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WCopyDialog(object):
    def setupUi(self, WCopyDialog):
        WCopyDialog.setObjectName("WCopyDialog")
        WCopyDialog.resize(349, 130)
        self.w_buttonBox = QtWidgets.QDialogButtonBox(WCopyDialog)
        self.w_buttonBox.setGeometry(QtCore.QRect(20, 80, 311, 32))
        self.w_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.w_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.w_buttonBox.setObjectName("w_buttonBox")
        self.w_runout_title = QtWidgets.QLabel(WCopyDialog)
        self.w_runout_title.setGeometry(QtCore.QRect(10, 10, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.w_runout_title.setFont(font)
        self.w_runout_title.setAlignment(QtCore.Qt.AlignCenter)
        self.w_runout_title.setWordWrap(True)
        self.w_runout_title.setObjectName("w_runout_title")

        self.retranslateUi(WCopyDialog)
        self.w_buttonBox.accepted.connect(WCopyDialog.accept)
        self.w_buttonBox.rejected.connect(WCopyDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(WCopyDialog)

    def retranslateUi(self, WCopyDialog):
        _translate = QtCore.QCoreApplication.translate
        WCopyDialog.setWindowTitle(_translate("WCopyDialog", "Dialog"))
        self.w_runout_title.setText(_translate("WCopyDialog", "Copying file to local cache..."))
