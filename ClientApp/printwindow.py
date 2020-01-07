from __future__ import division
from builtins import str
from past.utils import old_div
from PyQt5.QtCore import Qt, pyqtSignal
from .qt.printwindow import *
from .fsutils.subfilesystem import *
from .fsutils.file import *
from .filelistmanager import FileListManager

class PrintWindow(QtWidgets.QWidget, Ui_PrintWindow):

    # Create the Qt signals we're going to use for updating the list
    # of USB files. Each signal takes a single argument, which is the
    # path to the newly mounted (created) or unmounted (deleted)
    # directory.

    # create_signal = pyqtSignal(str)
    # delete_signal = pyqtSignal(str)
    update_signal = pyqtSignal(str)
    sdfile_signal = pyqtSignal(list)

    def __init__(self, printer_if, temp_pop, personality, parent=None):
        super(PrintWindow, self).__init__()

        # Connect slots to the signals
        # self.create_signal.connect(self.update_usb_create)
        # self.delete_signal.connect(self.update_usb_delete)
        self.update_signal.connect(self.update_local)
        self.sdfile_signal.connect(self.updatefiles)

        # Set up the rest of the UI
        self.setupUi(self)
        self.printer_if = printer_if

        self.printer_if.set_file_list_update_callback(self.sd_file_list_update_callback)
        # print("Setting print finished callback")
        self.printer_if.set_print_finished_callback(self.print_finished_callback)
        
        # self.serial = serial
        # self.serial.data.updatefiles.connect(self.updatefiles)

#        self.update_signal_
        
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
        self.sd_pushbutton_print.clicked.connect(self.sd_start_print)
        self.ActivePrint.clicked.connect(self.activeprintpop)
        self.StopPrint.clicked.connect(self.stopprint)
        self.ActivePrint.setEnabled(False)
        self.StopPrint.setEnabled(False)
        self.sd_pushbutton_print.setEnabled(False)
        # self.serial.data.notprinting.connect(self.notprinting)
        # self.serial.data.printfinished.connect(self.finished)

        self.SDFileList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.SDFileList.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.SDFileList.verticalHeader().hide()
        # Stretch out the horizontal header to take up the entire view
        header = self.SDFileList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.SDFileList.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.SDFileList.verticalHeader().setDefaultSectionSize(50)
        self.SDFileList.verticalScrollBar().setStyleSheet(
            "QScrollBar::vertical{ width: 40px; }")

        tabWidth = (old_div(self.tabWidget.width(), 3))-24
        self.tabWidget.setStyleSheet(self.tabWidget.styleSheet(
        ) + "QTabBar::tab { width: " + str(tabWidth) + "px; height: 35px; font-size: 12pt;}")

        # Set up the list of USB files
        self.usb_file_manager = FileListManager(self.USBFileList,
                                                self.personality.watchpoint,
                                                self.usb_pathlabel,
                                                self.usb_pushbutton_up,
                                                self.usb_pushbutton_open,
                                                self.usb_pushbutton_print)

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

        self.loc_subdir = SubFileSystem(self.personality.localpath)
        self.loc_pathlabel.setText(self.loc_subdir.abspath)

        self.sd_pushbutton_print.clicked.connect(self.local_start_print)
        self.sd_pushbutton_print.setEnabled(False)

        # self.sd_pathlabel.setText("Files on ")
        self.clearlocalfiles()
        self.updatelocalfiles()
        self.update_loc_button_states()

    def set_usb_mount_signals(self, tuple):
        (create_signal, delete_signal) = tuple
        create_signal.connect(self.update_usb_create)
        delete_signal.connect(self.update_usb_delete)

    def set_usb_content_signal(self, signal):
        signal.connect(self.update_usb_content)

    def update_usb_create(self, path):
        self.usb_file_manager.update_create(path)

    def update_usb_delete(self, path):
        self.usb_file_manager.clear_files()

    def update_usb_content(self, path):
        self.usb_file_manager.update_files()

    def update_local(self, path):
        self.clearlocalfiles()
        self.updatelocalfiles()

    def scansd(self):
        self.printer_if.release_sd_card();
        self.printer_if.init_sd_card();
        self.printer_if.list_sd_card();

    def sd_file_list_update_callback(self, sd_file_list):
        self.sdfile_signal.emit(sd_file_list)
#        self.updatefiles(sd_file_list)

    def updatefiles(self, file_list):
        self.SDFileList.clearContents()
        self.SDFileList.setRowCount(0)
        
        for (filename, filesize) in file_list:
            rowpos = self.SDFileList.rowCount()

            self.SDFileList.insertRow(rowpos)
            file_wid = QtWidgets.QTableWidgetItem(filename)
            file_wid.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            size_wid = QtWidgets.QTableWidgetItem(str(filesize))
            size_wid.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.SDFileList.setItem(rowpos, 0, file_wid)
            self.SDFileList.setItem(rowpos, 1, size_wid)

        self.sd_pushbutton_print.setEnabled(True)

    def clearlocalfiles(self):
        self.LocalFileList.clearContents()
        self.LocalFileList.setRowCount(0)

    def updatelocalfiles(self):
        self.LocalFileList.clearContents()
        self.LocalFileList.setRowCount(0)

        files = self.loc_subdir.list()

        for localfile in files:
            rowpos = self.LocalFileList.rowCount()

            self.LocalFileList.insertRow(rowpos)

            file = QtWidgets.QTableWidgetItem(localfile.displayname)
            file.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            if localfile.type == 'f':
                size_str = str(localfile.size)
            else:
                size_str = ""

            size = QtWidgets.QTableWidgetItem(size_str)
            size.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.LocalFileList.setItem(rowpos, 0, file)
            self.LocalFileList.setItem(rowpos, 1, size)

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
        self.sd_pushbutton_print.setEnabled(True)
        self.ScanSD.setEnabled(True)
        # Why?:
        # self.SDFileList.setRowCount(0)
        self.parent.Control.setEnabled(True)
        ## self.serial.data.changestatus("ON")

    def sd_start_print(self):
        selected = self.SDFileList.currentRow()
        selected_file_item = self.SDFileList.item(selected, 0)
        selected_file = selected_file_item.text()
        # print("Printing <%s>" %(selected_file))
        if selected_file != None:
            self.printer_if.select_sd_file(selected_file)
            self.printer_if.start_print()

            self.sd_pushbutton_print.setEnabled(False)
            self.ActivePrint.setEnabled(True)
            self.StopPrint.setEnabled(True)
            self.ScanSD.setEnabled(False)

            self.temp_pop.activeprint()
            self.temp_pop.update_parameters()
            self.temp_pop.ActivePrintWid.FileProgress.setValue(0)
            self.parent.Control.setEnabled(False)

    def local_start_print(self):
        selected = self.LocalFileList.currentRow()
        selected_file_item = self.LocalFileList.item(selected, 0)

        if selected_file_item is None:
            return

        selected_file = selected_file_item.text()
        print("Printing local <%s>" %(selected_file))

        if selected_file != None:
            # self.printer_if.select_sd_file(selected_file)
            # self.printer_if.start_print()

            self.local_pushbutton_print.setEnabled(False)
            self.ActivePrint.setEnabled(True)
            self.StopPrint.setEnabled(True)
            self.ScanSD.setEnabled(False)

            self.temp_pop.activeprint()
            self.temp_pop.update_parameters()
            self.temp_pop.ActivePrintWid.FileProgress.setValue(0)
            self.parent.Control.setEnabled(False)
        

    def get_selected_widget_file(self, list_widget, subdir):
    
        foolist = list_widget.selectedItems()

        if len(foolist) < 1:
            return (-1, None, None)

        selected_row = list_widget.currentRow()

        if selected_row == -1:
            return (-1, None, None)

        selected_file = subdir.files[selected_row]
        selected_item = list_widget.currentItem()

        return (selected_row, selected_file, selected_item)


    def get_selected_loc_file(self):
        return self.get_selected_widget_file(self.LocalFileList, self.loc_subdir)

    def activeprintpop(self):
        if self.fullscreen:
            self.temp_pop.showFullScreen()
        else:
            self.temp_pop.show()

    def update_loc_button_states_none(self):
        self.loc_pushbutton_up.setEnabled(False)
        self.loc_pushbutton_open.setEnabled(False)
        self.loc_pushbutton_print.setEnabled(False)

    def update_loc_button_states(self):
        selected_row, selected_file, selected_item = self.get_selected_loc_file()

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
        selected_row, selected_file, selected_item = self.get_selected_loc_file()

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
        print("item clicked")
        row = self.USBFileList.currentRow()
        self.update_usb_button_states()

    def itemDoubleClicked(self):
        self.open_usb_subdir()
