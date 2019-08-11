# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/addlabelwindow.ui',
# licensing of 'qt/addlabelwindow.ui' applies.
#
# Created: Fri Aug  2 12:33:16 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_addlabel(object):
    def setupUi(self, addlabel):
        addlabel.setObjectName("addlabel")
        addlabel.resize(300, 102)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(addlabel.sizePolicy().hasHeightForWidth())
        addlabel.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(addlabel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Instructions = QtWidgets.QLabel(addlabel)
        self.Instructions.setMaximumSize(QtCore.QSize(16777215, 18))
        self.Instructions.setObjectName("Instructions")
        self.verticalLayout.addWidget(self.Instructions)
        self.LabelInput = QtWidgets.QTextEdit(addlabel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LabelInput.sizePolicy().hasHeightForWidth())
        self.LabelInput.setSizePolicy(sizePolicy)
        self.LabelInput.setMaximumSize(QtCore.QSize(16777215, 30))
        self.LabelInput.setObjectName("LabelInput")
        self.verticalLayout.addWidget(self.LabelInput)
        self.Button = QtWidgets.QDialogButtonBox(addlabel)
        self.Button.setOrientation(QtCore.Qt.Horizontal)
        self.Button.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.Button.setObjectName("Button")
        self.verticalLayout.addWidget(self.Button)

        self.retranslateUi(addlabel)
        QtCore.QMetaObject.connectSlotsByName(addlabel)

    def retranslateUi(self, addlabel):
        addlabel.setWindowTitle(QtWidgets.QApplication.translate("addlabel", "Add Label", None, -1))
        self.Instructions.setText(QtWidgets.QApplication.translate("addlabel", "Add a Label to the Dashboard", None, -1))
        self.LabelInput.setHtml(QtWidgets.QApplication.translate("addlabel", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, -1))

