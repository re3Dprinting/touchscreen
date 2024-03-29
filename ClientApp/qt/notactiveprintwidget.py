# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notactiveprintwidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NotActivePrintWidget(object):
    def setupUi(self, NotActivePrintWidget):
        NotActivePrintWidget.setObjectName("NotActivePrintWidget")
        NotActivePrintWidget.resize(800, 480)
        NotActivePrintWidget.setMaximumSize(QtCore.QSize(800, 480))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(NotActivePrintWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.PreheatPLA = QtWidgets.QLabel(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PreheatPLA.sizePolicy().hasHeightForWidth())
        self.PreheatPLA.setSizePolicy(sizePolicy)
        self.PreheatPLA.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.PreheatPLA.setObjectName("PreheatPLA")
        self.verticalLayout.addWidget(self.PreheatPLA)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.w_pushbutton_m0_extruder1 = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m0_extruder1.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m0_extruder1.setSizePolicy(sizePolicy)
        self.w_pushbutton_m0_extruder1.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m0_extruder1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m0_extruder1.setFont(font)
        self.w_pushbutton_m0_extruder1.setToolTip("")
        self.w_pushbutton_m0_extruder1.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/Extruder_2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.w_pushbutton_m0_extruder1.setIcon(icon)
        self.w_pushbutton_m0_extruder1.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m0_extruder1.setObjectName("w_pushbutton_m0_extruder1")
        self.gridLayout.addWidget(self.w_pushbutton_m0_extruder1, 0, 1, 1, 1)
        self.w_pushbutton_m0_bed = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m0_bed.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m0_bed.setSizePolicy(sizePolicy)
        self.w_pushbutton_m0_bed.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m0_bed.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m0_bed.setFont(font)
        self.w_pushbutton_m0_bed.setToolTip("")
        self.w_pushbutton_m0_bed.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/img/Heated_Bed.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.w_pushbutton_m0_bed.setIcon(icon1)
        self.w_pushbutton_m0_bed.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m0_bed.setObjectName("w_pushbutton_m0_bed")
        self.gridLayout.addWidget(self.w_pushbutton_m0_bed, 1, 0, 1, 1)
        self.w_pushbutton_m0_all = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m0_all.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m0_all.setSizePolicy(sizePolicy)
        self.w_pushbutton_m0_all.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m0_all.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m0_all.setFont(font)
        self.w_pushbutton_m0_all.setToolTip("")
        self.w_pushbutton_m0_all.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/img/Extruder_with_Bed.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.w_pushbutton_m0_all.setIcon(icon2)
        self.w_pushbutton_m0_all.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m0_all.setObjectName("w_pushbutton_m0_all")
        self.gridLayout.addWidget(self.w_pushbutton_m0_all, 1, 1, 1, 1)
        self.w_pushbutton_m0_extruder0 = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m0_extruder0.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m0_extruder0.setSizePolicy(sizePolicy)
        self.w_pushbutton_m0_extruder0.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m0_extruder0.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m0_extruder0.setFont(font)
        self.w_pushbutton_m0_extruder0.setToolTip("")
        self.w_pushbutton_m0_extruder0.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/img/img/Extruder_1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.w_pushbutton_m0_extruder0.setIcon(icon3)
        self.w_pushbutton_m0_extruder0.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m0_extruder0.setObjectName("w_pushbutton_m0_extruder0")
        self.gridLayout.addWidget(self.w_pushbutton_m0_extruder0, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMinimumSize(QtCore.QSize(35, 0))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.PreheatPC = QtWidgets.QLabel(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PreheatPC.sizePolicy().hasHeightForWidth())
        self.PreheatPC.setSizePolicy(sizePolicy)
        self.PreheatPC.setObjectName("PreheatPC")
        self.verticalLayout_2.addWidget(self.PreheatPC)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.w_pushbutton_m1_extruder0 = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m1_extruder0.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m1_extruder0.setSizePolicy(sizePolicy)
        self.w_pushbutton_m1_extruder0.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m1_extruder0.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m1_extruder0.setFont(font)
        self.w_pushbutton_m1_extruder0.setToolTip("")
        self.w_pushbutton_m1_extruder0.setText("")
        self.w_pushbutton_m1_extruder0.setIcon(icon3)
        self.w_pushbutton_m1_extruder0.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m1_extruder0.setObjectName("w_pushbutton_m1_extruder0")
        self.gridLayout_2.addWidget(self.w_pushbutton_m1_extruder0, 0, 0, 1, 1)
        self.w_pushbutton_m1_extruder1 = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m1_extruder1.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m1_extruder1.setSizePolicy(sizePolicy)
        self.w_pushbutton_m1_extruder1.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m1_extruder1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m1_extruder1.setFont(font)
        self.w_pushbutton_m1_extruder1.setToolTip("")
        self.w_pushbutton_m1_extruder1.setText("")
        self.w_pushbutton_m1_extruder1.setIcon(icon)
        self.w_pushbutton_m1_extruder1.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m1_extruder1.setObjectName("w_pushbutton_m1_extruder1")
        self.gridLayout_2.addWidget(self.w_pushbutton_m1_extruder1, 0, 1, 1, 1)
        self.w_pushbutton_m1_bed = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m1_bed.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m1_bed.setSizePolicy(sizePolicy)
        self.w_pushbutton_m1_bed.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m1_bed.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m1_bed.setFont(font)
        self.w_pushbutton_m1_bed.setToolTip("")
        self.w_pushbutton_m1_bed.setText("")
        self.w_pushbutton_m1_bed.setIcon(icon1)
        self.w_pushbutton_m1_bed.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m1_bed.setObjectName("w_pushbutton_m1_bed")
        self.gridLayout_2.addWidget(self.w_pushbutton_m1_bed, 1, 0, 1, 1)
        self.w_pushbutton_m1_all = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m1_all.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m1_all.setSizePolicy(sizePolicy)
        self.w_pushbutton_m1_all.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m1_all.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m1_all.setFont(font)
        self.w_pushbutton_m1_all.setToolTip("")
        self.w_pushbutton_m1_all.setText("")
        self.w_pushbutton_m1_all.setIcon(icon2)
        self.w_pushbutton_m1_all.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m1_all.setObjectName("w_pushbutton_m1_all")
        self.gridLayout_2.addWidget(self.w_pushbutton_m1_all, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.line_2 = QtWidgets.QFrame(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setMinimumSize(QtCore.QSize(35, 0))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.PreheatPETG = QtWidgets.QLabel(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PreheatPETG.sizePolicy().hasHeightForWidth())
        self.PreheatPETG.setSizePolicy(sizePolicy)
        self.PreheatPETG.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.PreheatPETG.setObjectName("PreheatPETG")
        self.verticalLayout_3.addWidget(self.PreheatPETG)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setHorizontalSpacing(6)
        self.gridLayout_3.setVerticalSpacing(3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.w_pushbutton_m2_extruder1 = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m2_extruder1.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m2_extruder1.setSizePolicy(sizePolicy)
        self.w_pushbutton_m2_extruder1.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m2_extruder1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m2_extruder1.setFont(font)
        self.w_pushbutton_m2_extruder1.setToolTip("")
        self.w_pushbutton_m2_extruder1.setText("")
        self.w_pushbutton_m2_extruder1.setIcon(icon)
        self.w_pushbutton_m2_extruder1.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m2_extruder1.setObjectName("w_pushbutton_m2_extruder1")
        self.gridLayout_3.addWidget(self.w_pushbutton_m2_extruder1, 0, 1, 1, 1)
        self.w_pushbutton_m2_extruder0 = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m2_extruder0.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m2_extruder0.setSizePolicy(sizePolicy)
        self.w_pushbutton_m2_extruder0.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m2_extruder0.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m2_extruder0.setFont(font)
        self.w_pushbutton_m2_extruder0.setToolTip("")
        self.w_pushbutton_m2_extruder0.setText("")
        self.w_pushbutton_m2_extruder0.setIcon(icon3)
        self.w_pushbutton_m2_extruder0.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m2_extruder0.setObjectName("w_pushbutton_m2_extruder0")
        self.gridLayout_3.addWidget(self.w_pushbutton_m2_extruder0, 0, 0, 1, 1)
        self.w_pushbutton_m2_bed = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m2_bed.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m2_bed.setSizePolicy(sizePolicy)
        self.w_pushbutton_m2_bed.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m2_bed.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m2_bed.setFont(font)
        self.w_pushbutton_m2_bed.setToolTip("")
        self.w_pushbutton_m2_bed.setText("")
        self.w_pushbutton_m2_bed.setIcon(icon1)
        self.w_pushbutton_m2_bed.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m2_bed.setObjectName("w_pushbutton_m2_bed")
        self.gridLayout_3.addWidget(self.w_pushbutton_m2_bed, 1, 0, 1, 1)
        self.w_pushbutton_m2_all = QtWidgets.QPushButton(NotActivePrintWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_m2_all.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_m2_all.setSizePolicy(sizePolicy)
        self.w_pushbutton_m2_all.setMinimumSize(QtCore.QSize(75, 70))
        self.w_pushbutton_m2_all.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.w_pushbutton_m2_all.setFont(font)
        self.w_pushbutton_m2_all.setToolTip("")
        self.w_pushbutton_m2_all.setText("")
        self.w_pushbutton_m2_all.setIcon(icon2)
        self.w_pushbutton_m2_all.setIconSize(QtCore.QSize(59, 59))
        self.w_pushbutton_m2_all.setObjectName("w_pushbutton_m2_all")
        self.gridLayout_3.addWidget(self.w_pushbutton_m2_all, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.BottomBar = QtWidgets.QWidget(NotActivePrintWidget)
        self.BottomBar.setObjectName("BottomBar")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.BottomBar)
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
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
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/img/img/Small_arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back.setIcon(icon4)
        self.Back.setIconSize(QtCore.QSize(55, 55))
        self.Back.setObjectName("Back")
        self.horizontalLayout_3.addWidget(self.Back)
        spacerItem = QtWidgets.QSpacerItem(590, 45, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.w_pushbutton_cooldown = QtWidgets.QPushButton(self.BottomBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_cooldown.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_cooldown.setSizePolicy(sizePolicy)
        self.w_pushbutton_cooldown.setMinimumSize(QtCore.QSize(85, 65))
        self.w_pushbutton_cooldown.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.w_pushbutton_cooldown.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/img/img/Temperature.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.w_pushbutton_cooldown.setIcon(icon5)
        self.w_pushbutton_cooldown.setIconSize(QtCore.QSize(55, 55))
        self.w_pushbutton_cooldown.setObjectName("w_pushbutton_cooldown")
        self.horizontalLayout_3.addWidget(self.w_pushbutton_cooldown)
        self.w_pushbutton_fan = QtWidgets.QPushButton(self.BottomBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_pushbutton_fan.sizePolicy().hasHeightForWidth())
        self.w_pushbutton_fan.setSizePolicy(sizePolicy)
        self.w_pushbutton_fan.setMinimumSize(QtCore.QSize(85, 65))
        self.w_pushbutton_fan.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.w_pushbutton_fan.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/img/img/Fans_off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.w_pushbutton_fan.setIcon(icon6)
        self.w_pushbutton_fan.setIconSize(QtCore.QSize(65, 65))
        self.w_pushbutton_fan.setObjectName("w_pushbutton_fan")
        self.horizontalLayout_3.addWidget(self.w_pushbutton_fan)
        self.verticalLayout_4.addWidget(self.BottomBar)

        self.retranslateUi(NotActivePrintWidget)
        QtCore.QMetaObject.connectSlotsByName(NotActivePrintWidget)

    def retranslateUi(self, NotActivePrintWidget):
        _translate = QtCore.QCoreApplication.translate
        NotActivePrintWidget.setWindowTitle(_translate("NotActivePrintWidget", "TemperatureWindow"))
        self.PreheatPLA.setText(_translate("NotActivePrintWidget", "Pre-Heat PLA"))
        self.PreheatPC.setText(_translate("NotActivePrintWidget", "Pre-Heat PC"))
        self.PreheatPETG.setText(_translate("NotActivePrintWidget", "Pre-Heat PETG"))
import img_rc
