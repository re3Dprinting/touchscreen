# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/module_moreinfo.ui',
# licensing of 'qt/module_moreinfo.ui' applies.
#
# Created: Tue Jul 30 17:26:22 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MoreInfoWindow(object):
    def setupUi(self, MoreInfoWindow):
        MoreInfoWindow.setObjectName("MoreInfoWindow")
        MoreInfoWindow.resize(375, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MoreInfoWindow.sizePolicy().hasHeightForWidth())
        MoreInfoWindow.setSizePolicy(sizePolicy)
        MoreInfoWindow.setMinimumSize(QtCore.QSize(375, 400))
        MoreInfoWindow.setMaximumSize(QtCore.QSize(375, 400))
        self.verticalLayout = QtWidgets.QVBoxLayout(MoreInfoWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.DataOutput = QtWidgets.QTextBrowser(MoreInfoWindow)
        self.DataOutput.setObjectName("DataOutput")
        self.verticalLayout.addWidget(self.DataOutput)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.VersionText = QtWidgets.QLabel(MoreInfoWindow)
        self.VersionText.setMaximumSize(QtCore.QSize(120, 40))
        self.VersionText.setObjectName("VersionText")
        self.horizontalLayout_2.addWidget(self.VersionText)
        self.VersionInput = QtWidgets.QTextEdit(MoreInfoWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VersionInput.sizePolicy().hasHeightForWidth())
        self.VersionInput.setSizePolicy(sizePolicy)
        self.VersionInput.setMaximumSize(QtCore.QSize(120, 30))
        self.VersionInput.setObjectName("VersionInput")
        self.horizontalLayout_2.addWidget(self.VersionInput)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.NumberText = QtWidgets.QLabel(MoreInfoWindow)
        self.NumberText.setMaximumSize(QtCore.QSize(120, 40))
        self.NumberText.setObjectName("NumberText")
        self.horizontalLayout.addWidget(self.NumberText)
        self.NumberInput = QtWidgets.QTextEdit(MoreInfoWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NumberInput.sizePolicy().hasHeightForWidth())
        self.NumberInput.setSizePolicy(sizePolicy)
        self.NumberInput.setMaximumSize(QtCore.QSize(120, 30))
        self.NumberInput.setObjectName("NumberInput")
        self.horizontalLayout.addWidget(self.NumberInput)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Button = QtWidgets.QDialogButtonBox(MoreInfoWindow)
        self.Button.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.Button.setObjectName("Button")
        self.verticalLayout.addWidget(self.Button)

        self.retranslateUi(MoreInfoWindow)
        QtCore.QMetaObject.connectSlotsByName(MoreInfoWindow)

    def retranslateUi(self, MoreInfoWindow):
        MoreInfoWindow.setWindowTitle(QtWidgets.QApplication.translate("MoreInfoWindow", "Dialog", None, -1))
        self.VersionText.setText(QtWidgets.QApplication.translate("MoreInfoWindow", "Gigabot Version :", None, -1))
        self.NumberText.setText(QtWidgets.QApplication.translate("MoreInfoWindow", "Gigabot Number :", None, -1))

