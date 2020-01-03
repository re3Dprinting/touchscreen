from __future__ import division
from builtins import str
from past.utils import old_div
from PyQt5.QtCore import Qt
from .qt.printwindow import *
from .fsutils.subfilesystem import *
from .fsutils.file import *

class PrintWindow(QtWidgets.QWidget, Ui_PrintWindow):
    def __init__(self, printer_if, temp_pop, personality, parent=None):
        super(PrintWindow, self).__init__()
        self.setupUi(self)
        self.printer_if = printer_if

        self.printer_if.set_file_list_update_callback(self.sd_file_list_update_callback)
        # print("Setting print finished callback")
        self.printer_if.set_print_finished_callback(self.print_finished_callback)
        
        # self.serial = serial
        # self.serial.data.updatefiles.connect(self.updatefiles)
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
        # self.serial.data.notprinting.connect(self.notprinting)
        # self.serial.data.printfinished.connect(self.finished)

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

        tabWidth = (old_div(self.tabWidget.width(), 3))-24
        self.tabWidget.setStyleSheet(self.tabWidget.styleSheet(
        ) + "QTabBar::tab { width: " + str(tabWidth) + "px; height: 35px; font-size: 12pt;}")

        # Set up the list of USB files

        self.USBFileList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.USBFileList.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.USBFileList.verticalHeader().hide()

        header = self.USBFileList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.USBFileList.itemClicked.connect(self.itemClicked)
        self.USBFileList.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.usb_pushbutton_open.clicked.connect(self.open_usb_subdir)
        self.usb_pushbutton_up.clicked.connect(self.up_usb_dir)

        self.usb_subdir = SubFileSystem(self.personality.watchpoint)
        self.usb_pathlabel.setText(self.usb_subdir.abspath)

        # self.updateusbfiles()
        self.clearusbfiles()
        # self.sd_pathlabel.setText("Files on ")
        self.update_usb_button_states()

        # Set up the list of local files

        self.LocalFileList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.LocalFileList.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.LocalFileList.verticalHeader().hide()

        header = self.LocalFileList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.LocalFileList.itemClicked.connect(self.itemClicked)
        self.LocalFileList.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.loc_pushbutton_open.clicked.connect(self.open_loc_subdir)
        self.loc_pushbutton_up.clicked.connect(self.up_loc_dir)

        self.loc_subdir = SubFileSystem(self.personality.watchpoint)
        self.loc_pathlabel.setText(self.loc_subdir.abspath)

        # self.updateusbfiles()
        self.clearusbfiles()
        # self.sd_pathlabel.setText("Files on ")
        self.update_loc_button_states()

    def update_usb_create(self, path):
        # print("Create:", path)
        self.usb_pathlabel.setText(path)
        self.usb_subdir = SubFileSystem(path)
        self.updateusbfiles()
        self.update_usb_button_states()

    def update_usb_delete(self, path):
        print("Delete:", path)
#        self.usb_pathlabel.setText(self.usb_subdir.abspath)
        self.clearusbfiles()
        self.usb_pathlabel.setText("")

    def scansd(self):
        self.printer_if.release_sd_card();
        self.printer_if.init_sd_card();
        self.printer_if.list_sd_card();

    def sd_file_list_update_callback(self, sd_file_list):
        self.updatefiles(sd_file_list)

    def updatefiles(self, file_list):
        self.FileList.clearContents()
        self.FileList.setRowCount(0)
        
        for (filename, filesize) in file_list:
            rowpos = self.FileList.rowCount()

            self.FileList.insertRow(rowpos)
            file_wid = QtWidgets.QTableWidgetItem(filename)
            file_wid.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            size_wid = QtWidgets.QTableWidgetItem(str(filesize))
            size_wid.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.FileList.setItem(rowpos, 0, file_wid)
            self.FileList.setItem(rowpos, 1, size_wid)

        self.StartPrint.setEnabled(True)

    def updateusbfiles(self):
        self.USBFileList.clearContents()
        self.USBFileList.setRowCount(0)
        files = self.usb_subdir.list()

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

    def print_finished_callback(self):
        self.finished()

    def finished(self):
        self.notprinting()
        # self.serial.data.changestatus("ON")
        # Question for Noah: Why scan the SD here?
        # self.scansd()

    def stopprint(self):
        # self.serial.reset()
        self.printer_if.cancel_printing()
        self.notprinting()
        # self.serial.data.changestatus("ON")
        # self.serial.data.resetsettemps()

    def notprinting(self):
        self.temp_pop.notactiveprint()
        self.ActivePrint.setEnabled(False)
        self.StopPrint.setEnabled(False)
        self.StartPrint.setEnabled(True)
        self.ScanSD.setEnabled(True)
        # Why?:
        # self.FileList.setRowCount(0)
        self.parent.Control.setEnabled(True)
        ## self.serial.data.changestatus("ON")

    def startprint(self):
        selected = self.FileList.currentRow()
        selected_file_item = self.FileList.item(selected, 0)
        selected_file = selected_file_item.text()
        # print("Printing <%s>" %(selected_file))
        if selected_file != None:
            self.printer_if.select_sd_file(selected_file)
            self.printer_if.start_print()

            self.StartPrint.setEnabled(False)
            self.ActivePrint.setEnabled(True)
            self.StopPrint.setEnabled(True)
            self.ScanSD.setEnabled(False)

            self.temp_pop.activeprint()
            self.temp_pop.update_parameters()
            self.temp_pop.ActivePrintWid.FileProgress.setValue(0)
            self.parent.Control.setEnabled(False)

    def get_selected_file(self):
        selected_row = self.USBFileList.currentRow()
        if selected_row == -1:
            return (-1, None, None)

        selected_file = self.usb_subdir.files[selected_row]
        selected_item = self.USBFileList.currentItem()

        return (selected_row, selected_file, selected_item)

    def activeprintpop(self):
        if self.fullscreen:
            self.temp_pop.showFullScreen()
        else:
            self.temp_pop.show()

    def update_usb_button_states_none(self):
        self.usb_pushbutton_up.setEnabled(False)
        self.usb_pushbutton_open.setEnabled(False)
        self.usb_pushbutton_print.setEnabled(False)

    def update_usb_button_states(self):
        selected_row, selected_file, selected_item = self.get_selected_file()

        if self.usb_subdir.depth() > 0:
            self.usb_pushbutton_up.setEnabled(True)
        else:
            self.usb_pushbutton_up.setEnabled(False)

        if selected_row == -1:
            self.usb_pushbutton_open.setEnabled(False)
            self.usb_pushbutton_print.setEnabled(False)
            return

        if selected_file.type == 'd':
            self.usb_pushbutton_open.setEnabled(True)
            self.usb_pushbutton_print.setEnabled(False)

        elif selected_file.type == 'f':
            self.usb_pushbutton_open.setEnabled(False)
            self.usb_pushbutton_print.setEnabled(True)

    def open_usb_subdir(self):
        selected_row, selected_file, selected_item = self.get_selected_file()

        if selected_row is None:
            return

        if selected_file.type != 'd':
            return

        self.item_stack.append(selected_row)

        self.usb_subdir.cd(selected_file.name)
        self.updateusbfiles()
        self.showFileAndDeselect(0)
        self.update_usb_button_states()
        self.usb_pathlabel.setText(self.usb_subdir.abspath)

    def up_usb_dir(self):
        self.usb_subdir.up()
        self.updateusbfiles()

        selected_row = self.item_stack.pop()
        self.showFile(selected_row)

        self.update_usb_button_states()
        self.usb_pathlabel.setText(self.usb_subdir.abspath)

    def update_loc_button_states_none(self):
        self.loc_pushbutton_up.setEnabled(False)
        self.loc_pushbutton_open.setEnabled(False)
        self.loc_pushbutton_print.setEnabled(False)

    def update_loc_button_states(self):
        selected_row, selected_file, selected_item = self.get_selected_file()

        if self.loc_subdir.depth() > 0:
            self.loc_pushbutton_up.setEnabled(True)
        else:
            self.loc_pushbutton_up.setEnabled(False)

        if selected_row == -1:
            self.loc_pushbutton_open.setEnabled(False)
            self.loc_pushbutton_print.setEnabled(False)
            return

        if selected_file.type == 'd':
            self.loc_pushbutton_open.setEnabled(True)
            self.loc_pushbutton_print.setEnabled(False)

        elif selected_file.type == 'f':
            self.loc_pushbutton_open.setEnabled(False)
            self.loc_pushbutton_print.setEnabled(True)

    def open_loc_subdir(self):
        selected_row, selected_file, selected_item = self.get_selected_file()

        if selected_row is None:
            return

        if selected_file.type != 'd':
            return

        self.item_stack.append(selected_row)

        self.loc_subdir.cd(selected_file.name)
        self.updateusbfiles()
        self.showFileAndDeselect(0)
        self.update_loc_button_states()
        self.loc_pathlabel.setText(self.loc_subdir.abspath)

    def up_loc_dir(self):
        self.loc_subdir.up()
        self.updateusbfiles()

        selected_row = self.item_stack.pop()
        self.showFile(selected_row)

        self.update_loc_button_states()
        self.loc_pathlabel.setText(self.loc_subdir.abspath)

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
        self.update_usb_button_states()

    def itemDoubleClicked(self):
        self.open_usb_subdir()
