# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui',
# licensing of 'mainwindow.ui' applies.
#
# Created: Wed Jul 24 14:03:04 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1006, 520)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 10, 961, 461))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(290, 40, 301, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(600, 30, 71, 71))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("img/11168491_641487062653104_7353348191666353708_n.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 110, 881, 77))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.GigabotTitle = QtWidgets.QTextBrowser(self.horizontalLayoutWidget)
        self.GigabotTitle.setObjectName("GigabotTitle")
        self.horizontalLayout_2.addWidget(self.GigabotTitle)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(40, 150, 881, 181))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Serveroutput = QtWidgets.QTextBrowser(self.horizontalLayoutWidget_2)
        self.Serveroutput.setObjectName("Serveroutput")
        self.horizontalLayout_3.addWidget(self.Serveroutput)
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(740, 410, 193, 29))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1006, 22))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuAdd_Machine = QtWidgets.QMenu(self.menubar)
        self.menuAdd_Machine.setObjectName("menuAdd_Machine")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAdd_Machine = QtWidgets.QAction(MainWindow)
        self.actionAdd_Machine.setObjectName("actionAdd_Machine")
        self.actionAdd_Something_Else = QtWidgets.QAction(MainWindow)
        self.actionAdd_Something_Else.setObjectName("actionAdd_Something_Else")
        self.menuAdd_Machine.addAction(self.actionAdd_Machine)
        self.menuAdd_Machine.addAction(self.actionAdd_Something_Else)
        self.menubar.addAction(self.menuAdd_Machine.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Gigabot Dashboard", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Gigabot DashBoard", None, -1))
        self.GigabotTitle.setHtml(QtWidgets.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Gigabot #</p></body></html>", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "Start Server", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("MainWindow", "Quit", None, -1))
        self.menuAdd_Machine.setTitle(QtWidgets.QApplication.translate("MainWindow", "Add Machine", None, -1))
        self.actionAdd_Machine.setText(QtWidgets.QApplication.translate("MainWindow", "Add Machine", None, -1))
        self.actionAdd_Something_Else.setText(QtWidgets.QApplication.translate("MainWindow", "Add Something Else", None, -1))

