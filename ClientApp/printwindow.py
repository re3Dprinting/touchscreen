from __future__ import division
from builtins import str
from past.utils import old_div
from PyQt5.QtCore import Qt
from qt.printwindow import *
from fsutils.subfilesystem import *

class PrintWindow(QtWidgets.QWidget, Ui_PrintWindow):
        def __init__(self, serial, temp_pop, parent = None):
                super(PrintWindow, self).__init__()
                self.setupUi(self)
                self.serial = serial
                self.serial.data.updatefiles.connect(self.updatefiles)
                self.temp_pop = temp_pop
                self.parent = parent

                if parent.fullscreen: self.fullscreen = True
                else: self.fullscreen = False

                self.Back.clicked.connect(self.close)
                self.ScanSD.clicked.connect(self.scansd)
                self.StartPrint.clicked.connect(self.startprint)
                self.ActivePrint.clicked.connect(self.activeprintpop)
                self.StopPrint.clicked.connect(self.stopprint)
                self.ActivePrint.setEnabled(False)
                self.StopPrint.setEnabled(False)
                self.StartPrint.setEnabled(False)
                self.serial.data.notprinting.connect(self.notprinting)
                self.serial.data.printfinished.connect(self.finished)

                self.FileList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
                self.FileList.setSelectionMode(QtWidgets.QTableView.SingleSelection)
                self.FileList.verticalHeader().hide()
                #Stretch out the horizontal header to take up the entire view
                header = self.FileList.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
                self.FileList.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
                self.FileList.verticalHeader().setDefaultSectionSize(50)
                self.FileList.verticalScrollBar().setStyleSheet("QScrollBar::vertical{ width: 40px; }")


                # Set up the list of USB files

                self.USBFileList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
                self.USBFileList.setSelectionMode(QtWidgets.QTableView.SingleSelection)
                self.USBFileList.verticalHeader().hide()

                header = self.USBFileList.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

                # self.USBFileList.cellActivated.connect(self.cellActivated)
                # self.USBFileList.cellChanged.connect(self.cellChanged)
                # self.USBFileList.cellClicked.connect(self.cellClicked)
                # self.USBFileList.cellDoubleClicked.connect(self.cellDoubleClicked)
                # self.USBFileList.cellEntered.connect(self.cellEntered)
                # self.USBFileList.cellPressed.connect(self.cellPressed)
                # self.USBFileList.currentCellChanged.connect(self.currentCellChanged)
                self.USBFileList.currentItemChanged.connect(self.currentItemChanged)
                # self.USBFileList.itemActivated.connect(self.itemActivated)
                # self.USBFileList.itemChanged.connect(self.itemChanged)
                self.USBFileList.itemClicked.connect(self.itemClicked)
                # self.USBFileList.itemDoubleClicked.connect(self.itemDoubleClicked)
                # self.USBFileList.itemEntered.connect(self.itemEntered)
                # self.USBFileList.itemPressed.connect(self.itemPressed)
                # self.USBFileList.itemSelectionChanged.connect(self.itemSelectionChanged)

                tabWidth = (old_div(self.tabWidget.width(),2))-24
                self.tabWidget.setStyleSheet(self.tabWidget.styleSheet() +"QTabBar::tab { width: " + str(tabWidth) + "px; height: 35px; font-size: 12pt;}")

                self.subdir = SubFileSystem("/Users/jct")
                self.updateusbfiles()

        def scansd(self):
                self.serial.send_serial("M22 \r")
                self.serial.send_serial("M21 \r")
                self.serial.send_serial("M20 \r")

        def updatefiles(self):
                self.FileList.setRowCount(0)
                for f in self.serial.data.files:
                        rowpos = self.FileList.rowCount()

                        self.FileList.insertRow(rowpos)
                        file= QtWidgets.QTableWidgetItem(f)
                        file.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                        size= QtWidgets.QTableWidgetItem(self.serial.data.files[f])
                        size.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                        self.FileList.setItem(rowpos, 0, file)
                        self.FileList.setItem(rowpos, 1, size)
                self.StartPrint.setEnabled(True)

        def updateusbfiles(self):
                print("Updating USB files")
                files = self.subdir.list()

                for usbfile in files:
                        rowpos = self.USBFileList.rowCount()

                        self.USBFileList.insertRow(rowpos)

                        file = QtWidgets.QTableWidgetItem(usbfile.displayname)
                        file.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                        if usbfile.type == 'f':
                                size_str = str(usbfile.size);
                        else:
                                size_str = ""

                        size = QtWidgets.QTableWidgetItem(size_str)
                        size.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                        self.USBFileList.setItem(rowpos, 0, file)
                        self.USBFileList.setItem(rowpos, 1, size)
                        
                        
        
        def finished(self):
                self.notprinting()
                self.serial.data.changestatus("ON")
                self.scansd()

        def stopprint(self):
                self.serial.reset()
                self.notprinting()
                self.serial.data.changestatus("ON")
                self.serial.data.resetsettemps()

        def notprinting(self):
                self.temp_pop.notactiveprint()
                self.ActivePrint.setEnabled(False)
                self.StopPrint.setEnabled(False)
                self.StartPrint.setEnabled(True)
                self.FileList.setRowCount(0)
                self.parent.Control.setEnabled(True)
                #self.serial.data.changestatus("ON")

        def startprint(self):
                selected = self.FileList.currentRow()
                selected_file = self.FileList.item(selected,0)
                if selected_file != None:
                        self.serial.data.currentfile = selected_file.text()
                        self.serial.data.addtobuffer("FI", self.serial.data.currentfile)
                        self.serial.send_serial("M23 "+  selected_file.text())
                        self.serial.send_serial("M24 \r")
                        self.StartPrint.setEnabled(False)
                        self.ActivePrint.setEnabled(True)
                        self.StopPrint.setEnabled(True)
                        self.serial.data.changestatus("AC")
                        self.serial.send_serial("M155 S1")
                        self.serial.send_serial("M27 S5")
                        self.temp_pop.activeprint()
                        self.temp_pop.update_parameters()
                        self.temp_pop.ActivePrintWid.FileProgress.setValue(0)
                        self.parent.Control.setEnabled(False)


        def activeprintpop(self):
                if self.fullscreen: self.temp_pop.showFullScreen()
                else: self.temp_pop.show()              


                # else:
                #       self.output_serial("Please select a file")


        # def cellActivated(self):
        #         print("cellActivated")

        # def cellChanged(self):
        #         print("cellChanged")

        # def cellClicked(self):
        #         print("cellClicked")

        # def cellDoubleClicked(self):
        #         print("cellDoubleClicked")

        # def cellEntered(self):
        #         print("cellEntered")

        # def cellPressed(self):
        #         print("cellPressed")

        # def currentCellChanged(self):
        #         print("currentCellChanged")

        def currentItemChanged(self):
                row = self.USBFileList.currentRow()
                print("currentItemChanged", row)

        # def itemActivated(self):
        #         print("itemActivated")

        # def itemChanged(self):
        #         print("itemChanged")

        def itemClicked(self, table):
                row = self.USBFileList.currentRow()
                print("itemClicked ", row)

        # def itemDoubleClicked(self):
        #         print("itemDoubleClicked")

        # def itemEntered(self):
        #         print("itemEntered")

        # def itemPressed(self):
        #         print("itemPressed")

        # def itemSelectionChanged(self):
        #         print("itemSelectionChanged")

