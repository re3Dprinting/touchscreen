from __future__ import division
from builtins import str
from past.utils import old_div
from PyQt5.QtCore import Qt
from qt.printwindow import *
from fsutils.subfilesystem import *
from fsutils.file import *


class PrintWindow(QtWidgets.QWidget, Ui_PrintWindow):
    def __init__(self, serial, temp_pop, personality, parent=None):
        super(PrintWindow, self).__init__()
        self.setupUi(self)
        self.serial = serial
        self.serial.data.updatefiles.connect(self.updatefiles)
        self.temp_pop = temp_pop
        self.personality = personality
        self.parent = parent

        self.item_stack = []

        if parent.fullscreen:
            self.fullscreen = True
        else:
            self.fullscreen = False

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
        # Stretch out the horizontal header to take up the entire view
        header = self.FileList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.FileList.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.FileList.verticalHeader().setDefaultSectionSize(50)
        self.FileList.verticalScrollBar().setStyleSheet(
            "QScrollBar::vertical{ width: 40px; }")

        # Set up the list of USB files

        self.USBFileList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.USBFileList.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.USBFileList.verticalHeader().hide()

        header = self.USBFileList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.USBFileList.itemClicked.connect(self.itemClicked)
        self.USBFileList.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.pushbutton_open.clicked.connect(self.open_subdir)
        self.pushbutton_up.clicked.connect(self.up_dir)

        # tabWidth = (old_div(self.tabWidget.width(), 2))-24
        # self.tabWidget.setStyleSheet(self.tabWidget.styleSheet(
        # ) + "QTabBar::tab { width: " + str(tabWidth) + "px; height: 35px; font-size: 12pt;}")

        self.subdir = SubFileSystem(self.personality.watchpoint)
        self.pathlabel.setText(self.subdir.abspath)
        self.pathlabel1.setText("foobar")

        # self.updateusbfiles()
        self.clearusbfiles()
        self.pathlabel.setText("")
        self.update_button_states()

    def update_create(self, path):
        print("Create:", path)
        self.pathlabel.setText(path)
        self.subdir = SubFileSystem(path)
        self.updateusbfiles()
        self.update_button_states()

    def update_delete(self, path):
        print("Delete:", path)
#        self.pathlabel.setText(self.subdir.abspath)
        self.clearusbfiles()
        self.pathlabel.setText("")

    def scansd(self):
        self.serial.send_serial("M22 \r")
        self.serial.send_serial("M21 \r")
        self.serial.send_serial("M20 \r")

    def updatefiles(self):
        self.FileList.setRowCount(0)
        for f in self.serial.data.files:
            rowpos = self.FileList.rowCount()

            self.FileList.insertRow(rowpos)
            file = QtWidgets.QTableWidgetItem(f)
            file.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            size = QtWidgets.QTableWidgetItem(self.serial.data.files[f])
            size.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.FileList.setItem(rowpos, 0, file)
            self.FileList.setItem(rowpos, 1, size)
        self.StartPrint.setEnabled(True)

    def updateusbfiles(self):
        self.USBFileList.clearContents()
        self.USBFileList.setRowCount(0)
        files = self.subdir.list()

        for usbfile in files:
            rowpos = self.USBFileList.rowCount()

            self.USBFileList.insertRow(rowpos)

            file = QtWidgets.QTableWidgetItem(usbfile.displayname)
            file.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            if usbfile.type == 'f':
                size_str = str(usbfile.size)
            else:
                size_str = ""

            size = QtWidgets.QTableWidgetItem(size_str)
            size.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.USBFileList.setItem(rowpos, 0, file)
            self.USBFileList.setItem(rowpos, 1, size)

    def clearusbfiles(self):
        self.USBFileList.clearContents()
        self.USBFileList.setRowCount(0)
        

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
        # self.serial.data.changestatus("ON")

    def startprint(self):
        selected = self.FileList.currentRow()
        selected_file = self.FileList.item(selected, 0)
        if selected_file != None:
            self.serial.data.currentfile = selected_file.text()
            self.serial.data.addtobuffer("FI", self.serial.data.currentfile)
            self.serial.send_serial("M23 " + selected_file.text())
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

    def get_selected_file(self):
        selected_row = self.USBFileList.currentRow()
        if selected_row == -1:
            return (-1, None, None)

        selected_file = self.subdir.files[selected_row]
        selected_item = self.USBFileList.currentItem()

        return (selected_row, selected_file, selected_item)

    def activeprintpop(self):
        if self.fullscreen:
            self.temp_pop.showFullScreen()
        else:
            self.temp_pop.show()

    def update_button_states_none(self):
        self.pushbutton_up.setEnabled(False)
        self.pushbutton_open.setEnabled(False)
        self.pushbutton_print.setEnabled(False)

    def update_button_states(self):
        selected_row, selected_file, selected_item = self.get_selected_file()

        if self.subdir.depth() > 0:
            self.pushbutton_up.setEnabled(True)
        else:
            self.pushbutton_up.setEnabled(False)

        if selected_row == -1:
            self.pushbutton_open.setEnabled(False)
            self.pushbutton_print.setEnabled(False)
            return

        if selected_file.type == 'd':
            self.pushbutton_open.setEnabled(True)
            self.pushbutton_print.setEnabled(False)

        elif selected_file.type == 'f':
            self.pushbutton_open.setEnabled(False)
            self.pushbutton_print.setEnabled(True)

    def open_subdir(self):
        selected_row, selected_file, selected_item = self.get_selected_file()

        if selected_row is None:
            return

        if selected_file.type != 'd':
            return

        self.item_stack.append(selected_row)

        self.subdir.cd(selected_file.name)
        self.updateusbfiles()
        self.showFileAndDeselect(0)
        self.update_button_states()
        self.pathlabel.setText(self.subdir.abspath)

    def up_dir(self):
        self.subdir.up()
        self.updateusbfiles()

        selected_row = self.item_stack.pop()
        self.showFile(selected_row)

        self.update_button_states()
        self.pathlabel.setText(self.subdir.abspath)

    def showFile(self, selected_row):
        self.USBFileList.setCurrentCell(selected_row, 0)
        selected_item = self.USBFileList.currentItem()
        self.USBFileList.scrollToItem(selected_item)

    def showFileAndDeselect(self, selected_row):
        self.USBFileList.setCurrentCell(selected_row, 0)
        selected_item = self.USBFileList.currentItem()
        self.USBFileList.scrollToItem(selected_item)
        self.USBFileList.setCurrentItem(None)

    def itemClicked(self):
        row = self.USBFileList.currentRow()
        self.update_button_states()

    def itemDoubleClicked(self):
        self.open_subdir()
