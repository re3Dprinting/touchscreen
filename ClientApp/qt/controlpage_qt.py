# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'controlpage_qt.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ControlPage(object):
    def setupUi(self, ControlPage):
        ControlPage.setObjectName("ControlPage")
        ControlPage.resize(800, 448)
        ControlPage.setMaximumSize(QtCore.QSize(800, 448))
        self.YPos = QtWidgets.QPushButton(ControlPage)
        self.YPos.setGeometry(QtCore.QRect(170, 50, 91, 91))
        self.YPos.setMaximumSize(QtCore.QSize(100, 100))
        self.YPos.setFocusPolicy(QtCore.Qt.NoFocus)
        self.YPos.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/uparrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.YPos.setIcon(icon)
        self.YPos.setIconSize(QtCore.QSize(90, 90))
        self.YPos.setObjectName("YPos")
        self.YNeg = QtWidgets.QPushButton(ControlPage)
        self.YNeg.setGeometry(QtCore.QRect(170, 230, 91, 91))
        self.YNeg.setMaximumSize(QtCore.QSize(100, 100))
        self.YNeg.setFocusPolicy(QtCore.Qt.NoFocus)
        self.YNeg.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/downarrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.YNeg.setIcon(icon1)
        self.YNeg.setIconSize(QtCore.QSize(90, 90))
        self.YNeg.setObjectName("YNeg")
        self.XNeg = QtWidgets.QPushButton(ControlPage)
        self.XNeg.setGeometry(QtCore.QRect(79, 139, 91, 91))
        self.XNeg.setMaximumSize(QtCore.QSize(100, 100))
        self.XNeg.setFocusPolicy(QtCore.Qt.NoFocus)
        self.XNeg.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/leftarrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.XNeg.setIcon(icon2)
        self.XNeg.setIconSize(QtCore.QSize(90, 90))
        self.XNeg.setObjectName("XNeg")
        self.XPos = QtWidgets.QPushButton(ControlPage)
        self.XPos.setGeometry(QtCore.QRect(260, 140, 91, 91))
        self.XPos.setMaximumSize(QtCore.QSize(100, 100))
        self.XPos.setFocusPolicy(QtCore.Qt.NoFocus)
        self.XPos.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/rightarrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.XPos.setIcon(icon3)
        self.XPos.setIconSize(QtCore.QSize(90, 90))
        self.XPos.setObjectName("XPos")
        self.ZPos = QtWidgets.QPushButton(ControlPage)
        self.ZPos.setGeometry(QtCore.QRect(460, 140, 91, 91))
        self.ZPos.setMaximumSize(QtCore.QSize(100, 100))
        self.ZPos.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ZPos.setText("")
        self.ZPos.setIcon(icon1)
        self.ZPos.setIconSize(QtCore.QSize(90, 90))
        self.ZPos.setObjectName("ZPos")
        self.ZNeg = QtWidgets.QPushButton(ControlPage)
        self.ZNeg.setGeometry(QtCore.QRect(460, 50, 91, 91))
        self.ZNeg.setMaximumSize(QtCore.QSize(100, 100))
        self.ZNeg.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ZNeg.setText("")
        self.ZNeg.setIcon(icon)
        self.ZNeg.setIconSize(QtCore.QSize(90, 90))
        self.ZNeg.setObjectName("ZNeg")
        self.ENeg = QtWidgets.QPushButton(ControlPage)
        self.ENeg.setGeometry(QtCore.QRect(590, 50, 91, 91))
        self.ENeg.setMaximumSize(QtCore.QSize(100, 100))
        self.ENeg.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ENeg.setText("")
        self.ENeg.setIcon(icon)
        self.ENeg.setIconSize(QtCore.QSize(90, 90))
        self.ENeg.setObjectName("ENeg")
        self.EPos = QtWidgets.QPushButton(ControlPage)
        self.EPos.setGeometry(QtCore.QRect(590, 140, 91, 91))
        self.EPos.setMaximumSize(QtCore.QSize(100, 100))
        self.EPos.setFocusPolicy(QtCore.Qt.NoFocus)
        self.EPos.setText("")
        self.EPos.setIcon(icon1)
        self.EPos.setIconSize(QtCore.QSize(90, 90))
        self.EPos.setObjectName("EPos")
        self.label = QtWidgets.QLabel(ControlPage)
        self.label.setGeometry(QtCore.QRect(270, 270, 31, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(ControlPage)
        self.label_2.setGeometry(QtCore.QRect(360, 180, 41, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(ControlPage)
        self.label_3.setGeometry(QtCore.QRect(40, 170, 31, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(ControlPage)
        self.label_4.setGeometry(QtCore.QRect(140, 60, 41, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(ControlPage)
        self.label_5.setGeometry(QtCore.QRect(490, 240, 51, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(ControlPage)
        self.label_6.setGeometry(QtCore.QRect(490, 10, 41, 31))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(ControlPage)
        self.label_7.setGeometry(QtCore.QRect(620, 240, 51, 31))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(ControlPage)
        self.label_8.setGeometry(QtCore.QRect(620, 10, 41, 31))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(ControlPage)
        self.label_9.setGeometry(QtCore.QRect(720, 40, 61, 39))
        self.label_9.setObjectName("label_9")
        self.Back = QtWidgets.QPushButton(ControlPage)
        self.Back.setGeometry(QtCore.QRect(4, 346, 91, 91))
        self.Back.setMaximumSize(QtCore.QSize(100, 100))
        self.Back.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Back.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("img/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon4)
        self.Back.setIconSize(QtCore.QSize(100, 100))
        self.Back.setObjectName("Back")
        self.layoutWidget = QtWidgets.QWidget(ControlPage)
        self.layoutWidget.setGeometry(QtCore.QRect(440, 280, 361, 151))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.movex = QtWidgets.QLabel(self.layoutWidget)
        self.movex.setObjectName("movex")
        self.horizontalLayout.addWidget(self.movex)
        self.xm01 = QtWidgets.QPushButton(self.layoutWidget)
        self.xm01.setMinimumSize(QtCore.QSize(70, 30))
        self.xm01.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.xm01.setFont(font)
        self.xm01.setFocusPolicy(QtCore.Qt.NoFocus)
        self.xm01.setObjectName("xm01")
        self.horizontalLayout.addWidget(self.xm01)
        self.xm1 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xm1.sizePolicy().hasHeightForWidth())
        self.xm1.setSizePolicy(sizePolicy)
        self.xm1.setMinimumSize(QtCore.QSize(70, 30))
        self.xm1.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.xm1.setFont(font)
        self.xm1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.xm1.setObjectName("xm1")
        self.horizontalLayout.addWidget(self.xm1)
        self.xm10 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xm10.sizePolicy().hasHeightForWidth())
        self.xm10.setSizePolicy(sizePolicy)
        self.xm10.setMinimumSize(QtCore.QSize(70, 30))
        self.xm10.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.xm10.setFont(font)
        self.xm10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.xm10.setObjectName("xm10")
        self.horizontalLayout.addWidget(self.xm10)
        self.xm100 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xm100.sizePolicy().hasHeightForWidth())
        self.xm100.setSizePolicy(sizePolicy)
        self.xm100.setMinimumSize(QtCore.QSize(70, 30))
        self.xm100.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.xm100.setFont(font)
        self.xm100.setFocusPolicy(QtCore.Qt.NoFocus)
        self.xm100.setObjectName("xm100")
        self.horizontalLayout.addWidget(self.xm100)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.movey = QtWidgets.QLabel(self.layoutWidget)
        self.movey.setObjectName("movey")
        self.horizontalLayout_2.addWidget(self.movey)
        self.ym01 = QtWidgets.QPushButton(self.layoutWidget)
        self.ym01.setMinimumSize(QtCore.QSize(70, 30))
        self.ym01.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ym01.setFont(font)
        self.ym01.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ym01.setObjectName("ym01")
        self.horizontalLayout_2.addWidget(self.ym01)
        self.ym1 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ym1.sizePolicy().hasHeightForWidth())
        self.ym1.setSizePolicy(sizePolicy)
        self.ym1.setMinimumSize(QtCore.QSize(70, 30))
        self.ym1.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ym1.setFont(font)
        self.ym1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ym1.setObjectName("ym1")
        self.horizontalLayout_2.addWidget(self.ym1)
        self.ym10 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ym10.sizePolicy().hasHeightForWidth())
        self.ym10.setSizePolicy(sizePolicy)
        self.ym10.setMinimumSize(QtCore.QSize(70, 30))
        self.ym10.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ym10.setFont(font)
        self.ym10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ym10.setObjectName("ym10")
        self.horizontalLayout_2.addWidget(self.ym10)
        self.ym100 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ym100.sizePolicy().hasHeightForWidth())
        self.ym100.setSizePolicy(sizePolicy)
        self.ym100.setMinimumSize(QtCore.QSize(70, 30))
        self.ym100.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ym100.setFont(font)
        self.ym100.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ym100.setObjectName("ym100")
        self.horizontalLayout_2.addWidget(self.ym100)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.movez = QtWidgets.QLabel(self.layoutWidget)
        self.movez.setObjectName("movez")
        self.horizontalLayout_3.addWidget(self.movez)
        self.zm01 = QtWidgets.QPushButton(self.layoutWidget)
        self.zm01.setMinimumSize(QtCore.QSize(70, 30))
        self.zm01.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.zm01.setFont(font)
        self.zm01.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zm01.setObjectName("zm01")
        self.horizontalLayout_3.addWidget(self.zm01)
        self.zm1 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zm1.sizePolicy().hasHeightForWidth())
        self.zm1.setSizePolicy(sizePolicy)
        self.zm1.setMinimumSize(QtCore.QSize(70, 30))
        self.zm1.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.zm1.setFont(font)
        self.zm1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zm1.setObjectName("zm1")
        self.horizontalLayout_3.addWidget(self.zm1)
        self.zm10 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zm10.sizePolicy().hasHeightForWidth())
        self.zm10.setSizePolicy(sizePolicy)
        self.zm10.setMinimumSize(QtCore.QSize(70, 30))
        self.zm10.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.zm10.setFont(font)
        self.zm10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zm10.setObjectName("zm10")
        self.horizontalLayout_3.addWidget(self.zm10)
        self.zm100 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zm100.sizePolicy().hasHeightForWidth())
        self.zm100.setSizePolicy(sizePolicy)
        self.zm100.setMinimumSize(QtCore.QSize(70, 30))
        self.zm100.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.zm100.setFont(font)
        self.zm100.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zm100.setObjectName("zm100")
        self.horizontalLayout_3.addWidget(self.zm100)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.movee = QtWidgets.QLabel(self.layoutWidget)
        self.movee.setObjectName("movee")
        self.horizontalLayout_4.addWidget(self.movee)
        self.em01 = QtWidgets.QPushButton(self.layoutWidget)
        self.em01.setMinimumSize(QtCore.QSize(70, 30))
        self.em01.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.em01.setFont(font)
        self.em01.setFocusPolicy(QtCore.Qt.NoFocus)
        self.em01.setObjectName("em01")
        self.horizontalLayout_4.addWidget(self.em01)
        self.em1 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.em1.sizePolicy().hasHeightForWidth())
        self.em1.setSizePolicy(sizePolicy)
        self.em1.setMinimumSize(QtCore.QSize(70, 30))
        self.em1.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.em1.setFont(font)
        self.em1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.em1.setObjectName("em1")
        self.horizontalLayout_4.addWidget(self.em1)
        self.em10 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.em10.sizePolicy().hasHeightForWidth())
        self.em10.setSizePolicy(sizePolicy)
        self.em10.setMinimumSize(QtCore.QSize(70, 30))
        self.em10.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.em10.setFont(font)
        self.em10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.em10.setObjectName("em10")
        self.horizontalLayout_4.addWidget(self.em10)
        self.em100 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.em100.sizePolicy().hasHeightForWidth())
        self.em100.setSizePolicy(sizePolicy)
        self.em100.setMinimumSize(QtCore.QSize(70, 30))
        self.em100.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.em100.setFont(font)
        self.em100.setFocusPolicy(QtCore.Qt.NoFocus)
        self.em100.setObjectName("em100")
        self.horizontalLayout_4.addWidget(self.em100)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.layoutWidget1 = QtWidgets.QWidget(ControlPage)
        self.layoutWidget1.setGeometry(QtCore.QRect(730, 80, 41, 161))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.E1 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.E1.sizePolicy().hasHeightForWidth())
        self.E1.setSizePolicy(sizePolicy)
        self.E1.setMinimumSize(QtCore.QSize(30, 70))
        self.E1.setMaximumSize(QtCore.QSize(30, 70))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.E1.setFont(font)
        self.E1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.E1.setObjectName("E1")
        self.verticalLayout_2.addWidget(self.E1)
        self.E2 = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.E2.sizePolicy().hasHeightForWidth())
        self.E2.setSizePolicy(sizePolicy)
        self.E2.setMinimumSize(QtCore.QSize(30, 70))
        self.E2.setMaximumSize(QtCore.QSize(30, 70))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.E2.setFont(font)
        self.E2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.E2.setObjectName("E2")
        self.verticalLayout_2.addWidget(self.E2)
        self.HomeXY = QtWidgets.QPushButton(ControlPage)
        self.HomeXY.setGeometry(QtCore.QRect(50, 60, 50, 50))
        self.HomeXY.setMaximumSize(QtCore.QSize(100, 100))
        self.HomeXY.setFocusPolicy(QtCore.Qt.NoFocus)
        self.HomeXY.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("img/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.HomeXY.setIcon(icon5)
        self.HomeXY.setIconSize(QtCore.QSize(50, 50))
        self.HomeXY.setObjectName("HomeXY")
        self.DisableMotors = QtWidgets.QPushButton(ControlPage)
        self.DisableMotors.setGeometry(QtCore.QRect(350, 330, 71, 71))
        self.DisableMotors.setMaximumSize(QtCore.QSize(100, 100))
        self.DisableMotors.setFocusPolicy(QtCore.Qt.NoFocus)
        self.DisableMotors.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("img/disable_motor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DisableMotors.setIcon(icon6)
        self.DisableMotors.setIconSize(QtCore.QSize(70, 70))
        self.DisableMotors.setObjectName("DisableMotors")
        self.HomeZ = QtWidgets.QPushButton(ControlPage)
        self.HomeZ.setGeometry(QtCore.QRect(360, 60, 50, 50))
        self.HomeZ.setMaximumSize(QtCore.QSize(100, 100))
        self.HomeZ.setFocusPolicy(QtCore.Qt.NoFocus)
        self.HomeZ.setText("")
        self.HomeZ.setIcon(icon5)
        self.HomeZ.setIconSize(QtCore.QSize(50, 50))
        self.HomeZ.setObjectName("HomeZ")
        self.HomeAll = QtWidgets.QPushButton(ControlPage)
        self.HomeAll.setGeometry(QtCore.QRect(280, 330, 71, 71))
        self.HomeAll.setMaximumSize(QtCore.QSize(100, 100))
        self.HomeAll.setFocusPolicy(QtCore.Qt.NoFocus)
        self.HomeAll.setText("")
        self.HomeAll.setIcon(icon5)
        self.HomeAll.setIconSize(QtCore.QSize(55, 55))
        self.HomeAll.setObjectName("HomeAll")
        self.label_10 = QtWidgets.QLabel(ControlPage)
        self.label_10.setGeometry(QtCore.QRect(50, 20, 81, 39))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(ControlPage)
        self.label_11.setGeometry(QtCore.QRect(360, 20, 61, 39))
        self.label_11.setObjectName("label_11")
        self.widget = QtWidgets.QWidget(ControlPage)
        self.widget.setGeometry(QtCore.QRect(140, 340, 120, 91))
        self.widget.setObjectName("widget")
        self.w_lineedit_z_position = QtWidgets.QLineEdit(self.widget)
        self.w_lineedit_z_position.setGeometry(QtCore.QRect(30, 60, 71, 24))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.w_lineedit_z_position.sizePolicy().hasHeightForWidth())
        self.w_lineedit_z_position.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.w_lineedit_z_position.setFont(font)
        self.w_lineedit_z_position.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_lineedit_z_position.setInputMask("")
        self.w_lineedit_z_position.setText("")
        self.w_lineedit_z_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.w_lineedit_z_position.setObjectName("w_lineedit_z_position")
        self.w_label_position_x_3 = QtWidgets.QLabel(self.widget)
        self.w_label_position_x_3.setGeometry(QtCore.QRect(10, 60, 21, 24))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.w_label_position_x_3.setFont(font)
        self.w_label_position_x_3.setObjectName("w_label_position_x_3")
        self.w_label_position_x_2 = QtWidgets.QLabel(self.widget)
        self.w_label_position_x_2.setGeometry(QtCore.QRect(10, 30, 21, 24))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.w_label_position_x_2.setFont(font)
        self.w_label_position_x_2.setObjectName("w_label_position_x_2")
        self.w_lineedit_y_position = QtWidgets.QLineEdit(self.widget)
        self.w_lineedit_y_position.setGeometry(QtCore.QRect(30, 30, 71, 24))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.w_lineedit_y_position.sizePolicy().hasHeightForWidth())
        self.w_lineedit_y_position.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.w_lineedit_y_position.setFont(font)
        self.w_lineedit_y_position.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_lineedit_y_position.setInputMask("")
        self.w_lineedit_y_position.setText("")
        self.w_lineedit_y_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.w_lineedit_y_position.setObjectName("w_lineedit_y_position")
        self.w_label_position_x = QtWidgets.QLabel(self.widget)
        self.w_label_position_x.setGeometry(QtCore.QRect(10, 0, 21, 24))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.w_label_position_x.setFont(font)
        self.w_label_position_x.setObjectName("w_label_position_x")
        self.w_lineedit_x_position = QtWidgets.QLineEdit(self.widget)
        self.w_lineedit_x_position.setEnabled(True)
        self.w_lineedit_x_position.setGeometry(QtCore.QRect(30, 0, 71, 24))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.w_lineedit_x_position.sizePolicy().hasHeightForWidth())
        self.w_lineedit_x_position.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.w_lineedit_x_position.setFont(font)
        self.w_lineedit_x_position.setFocusPolicy(QtCore.Qt.NoFocus)
        self.w_lineedit_x_position.setInputMask("")
        self.w_lineedit_x_position.setText("")
        self.w_lineedit_x_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.w_lineedit_x_position.setObjectName("w_lineedit_x_position")

        self.retranslateUi(ControlPage)
        QtCore.QMetaObject.connectSlotsByName(ControlPage)

    def retranslateUi(self, ControlPage):
        _translate = QtCore.QCoreApplication.translate
        ControlPage.setWindowTitle(_translate("ControlPage", "ControlPage"))
        self.label.setText(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:20pt;\">-Y</span></p></body></html>"))
        self.label_2.setText(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:20pt;\">+X</span></p></body></html>"))
        self.label_3.setText(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:20pt;\">-X</span></p></body></html>"))
        self.label_4.setText(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:20pt;\">+Y</span></p></body></html>"))
        self.label_5.setText(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:20pt;\">+Z</span></p></body></html>"))
        self.label_6.setText(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:20pt;\">-Z</span></p></body></html>"))
        self.label_7.setText(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:20pt;\">+E</span></p></body></html>"))
        self.label_8.setText(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:20pt;\">-E</span></p></body></html>"))
        self.label_9.setText(_translate("ControlPage", "Extruder"))
        self.movex.setText(_translate("ControlPage", "Move X"))
        self.xm01.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.xm01.setText(_translate("ControlPage", "0.1"))
        self.xm1.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.xm1.setText(_translate("ControlPage", "1"))
        self.xm10.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.xm10.setText(_translate("ControlPage", "10"))
        self.xm100.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.xm100.setText(_translate("ControlPage", "100"))
        self.movey.setText(_translate("ControlPage", "Move Y"))
        self.ym01.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.ym01.setText(_translate("ControlPage", "0.1"))
        self.ym1.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.ym1.setText(_translate("ControlPage", "1"))
        self.ym10.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.ym10.setText(_translate("ControlPage", "10"))
        self.ym100.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.ym100.setText(_translate("ControlPage", "100"))
        self.movez.setText(_translate("ControlPage", "Move Z"))
        self.zm01.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.zm01.setText(_translate("ControlPage", "0.1"))
        self.zm1.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.zm1.setText(_translate("ControlPage", "1"))
        self.zm10.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.zm10.setText(_translate("ControlPage", "10"))
        self.zm100.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.zm100.setText(_translate("ControlPage", "100"))
        self.movee.setText(_translate("ControlPage", "Move E"))
        self.em01.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.em01.setText(_translate("ControlPage", "0.1"))
        self.em1.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.em1.setText(_translate("ControlPage", "1"))
        self.em10.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.em10.setText(_translate("ControlPage", "10"))
        self.em100.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.em100.setText(_translate("ControlPage", "100"))
        self.E1.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.E1.setText(_translate("ControlPage", "E0"))
        self.E2.setToolTip(_translate("ControlPage", "<html><head/><body><p><span style=\" font-size:24pt;\">0.1</span></p></body></html>"))
        self.E2.setText(_translate("ControlPage", "E1"))
        self.label_10.setText(_translate("ControlPage", "Home XY"))
        self.label_11.setText(_translate("ControlPage", "Home Z"))
        self.w_label_position_x_3.setText(_translate("ControlPage", "Z:"))
        self.w_label_position_x_2.setText(_translate("ControlPage", "Y:"))
        self.w_label_position_x.setText(_translate("ControlPage", "X:"))

