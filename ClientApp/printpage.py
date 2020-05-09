from __future__ import division
from basewindow import BaseWindow
from builtins import str
from constants import *

import logging

from past.utils import old_div
from PyQt5.QtCore import Qt, pyqtSignal

from octoprint.filemanager import storage
from octoprint.filemanager.util import DiskFileWrapper

from .qt.printpage_qt import *
from .fsutils.subfilesystem import *
from .fsutils.file import *
from .fsutils.mountpoint import MountPoint
from .filelistmanager import FileListManager
from basepage import BasePage

class PrintPage(BasePage, Ui_PrintPage):

    # Create the Qt signals we're going to use for updating the list
    # of USB files. Each signal takes a single argument, which is the
    # path to the newly mounted (created) or unmounted (deleted)
    # directory.

    # create_signal = pyqtSignal(str)
    # delete_signal = pyqtSignal(str)
    update_signal = pyqtSignal(str)
    sdfile_signal = pyqtSignal(list)

    def __init__(self, context):
        super(PrintPage, self).__init__()

        self.printer_if = context.printer_if
        self.personality = context.personality
        self.ui_controller = context.ui_controller

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("PrintPage __init__")

        # Connect slots to the signals
        # self.create_signal.connect(self.update_usb_create)
        # self.delete_signal.connect(self.update_usb_delete)
        self.update_signal.connect(self.update_local)
        self.sdfile_signal.connect(self.updatefiles)

        # Set up the rest of the UI

        self.setupUi(self)

        self.printer_if.set_file_list_update_callback(self.sd_file_list_update_callback)
        # print("Setting print finished callback")
        self.printer_if.set_print_finished_callback(self.print_finished_callback)

        # self.temp_pop = temp_pop

        self.item_stack = []

        self.pushbutton_back.clicked.connect(self.back)

        # if parent.fullscreen:
        #     self.fullscreen = True
        # else:
        #     self.fullscreen = False

        self.pushbutton_scan_sd.clicked.connect(self.scansd)
        self.pushbutton_sd_print.clicked.connect(self.sd_start_print)
        self.pushbutton_active_print.clicked.connect(self.activeprintpop)
        self.pushbutton_stop_print.clicked.connect(self.stopprint)
        self.pushbutton_active_print.setEnabled(False)
        self.pushbutton_stop_print.setEnabled(False)
        self.pushbutton_sd_print.setEnabled(False)
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
        self.usb_file_manager = FileListManager("USB",
                                                self.USBFileList,
                                                self.personality.watchpoint,
                                                self.usb_pathlabel,
                                                self.pushbutton_usb_up,
                                                self.pushbutton_usb_open,
                                                self.pushbutton_usb_print)

        self.pushbutton_usb_print.clicked.connect(self.usb_start_print)

        # Set up the list of local files

        self.local_file_manager = FileListManager("Local",
                                                  self.LocalFileList,
                                                  self.personality.localpath,
                                                  self.loc_pathlabel,
                                                  self.pushbutton_loc_up,
                                                  self.pushbutton_loc_open,
                                                  self.pushbutton_loc_print)

        self.local_file_manager.update_files()

        self.setbuttonstyle(self.pushbutton_back)
        self.pushbutton_loc_print.clicked.connect(self.local_start_print)

    def enable_control(self):
        home_page = self.ui_controller.get_page(k_home_page)
        home_page.pushbutton_control.setEnabled(True)

    def disable_control(self):
        home_page = self.ui_controller.get_page(k_home_page)
        home_page.pushbutton_control.setEnabled(False)

    def set_storage_manager(self, local_storage_manager):
        self.local_storage_manager = local_storage_manager
        
    def set_usb_mount_signals(self, tuple):
        (create_signal, delete_signal) = tuple
        create_signal.connect(self.update_usb_create)
        delete_signal.connect(self.update_usb_delete)

    def set_usb_content_signal(self, signal):
        signal.connect(self.update_usb_content)

    def update_usb_create(self, mountpoint):
        self._log("UPDATE_USB_CREATE: path <%s>, actual path <%s>" % (mountpoint.path, mountpoint.actual_path))
        self.usb_file_manager.update_create(mountpoint.path)

    def update_usb_delete(self, path):
        self.usb_file_manager.clear_files()

    def update_usb_content(self, path):
        self.usb_file_manager.update_files()

    def set_local_content_signal(self, signal):
        signal.connect(self.update_local_content)

    def update_local_content(self, path):
        print("Update local content called")
        self.local_file_manager.update_files()

    def update_local(self, path):
        self.clearlocalfiles()
        self.updatelocalfiles()

    def scansd(self):
        self._log("UI: User touched Scan")
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

        self.pushbutton_sd_print.setEnabled(True)

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
        self._log("UI: User touched Stop Print")
        # self.serial.reset()
        self.printer_if.cancel_printing()
        self.notprinting()
        # self.serial.data.changestatus("ON")
        # self.serial.data.resetsettemps()

    def notprinting(self):
        # self.temp_pop.notactiveprint()
        temperature_page = self.ui_controller.get_page(k_temperature_page)
        temperature_page.notactiveprint()
        self.pushbutton_active_print.setEnabled(False)
        self.pushbutton_stop_print.setEnabled(False)
        self.pushbutton_sd_print.setEnabled(True)
        self.pushbutton_usb_print.setEnabled(True)
        self.pushbutton_loc_print.setEnabled(True)
        self.pushbutton_scan_sd.setEnabled(True)
        # Why?:
        # self.SDFileList.setRowCount(0)
        #self.parent.Control.setEnabled(True)
        ## self.serial.data.changestatus("ON")
        self.enable_control()

    def temperature_active(self):
        temperature_page = self.ui_controller.get_page(k_temperature_page)
        temperature_page.activeprint()
        self._log("temperature_active: calling reset_parameters.")
        temperature_page.reset_parameters()
        temperature_page.set_progress(0)

    def temperature_inactive(self):
        temperature_page = self.ui_controller.get_page(k_temperature_page)
        temperature_page.notactiveprint()
        temperature_page.reset_parameters()
        temperature_page.set_progress(0)

    def sd_start_print(self):
        self._log("UI: User touched (SD) Start Print")
        selected = self.SDFileList.currentRow()
        selected_file_item = self.SDFileList.item(selected, 0)
        selected_file = selected_file_item.text()

        # print("Printing <%s>" %(selected_file))
        if selected_file != None:
            self.temperature_active()
            self.disable_control()

            self.printer_if.select_sd_file(selected_file)
            self.printer_if.start_print()

            self.pushbutton_sd_print.setEnabled(False)
            self.pushbutton_usb_print.setEnabled(False)
            self.pushbutton_loc_print.setEnabled(False)
            self.pushbutton_active_print.setEnabled(True)
            self.pushbutton_stop_print.setEnabled(True)
            self.pushbutton_scan_sd.setEnabled(False)

            # self.temp_pop.activeprint()
            # self.temp_pop.update_parameters()
            # self.temp_pop.ActivePrintWid.FileProgress.setValue(0)
            #self.parent.Control.setEnabled(False)

    def local_start_print(self):
        self._log("UI: User touched (Local) Start Print")
        (selected_row, selected_file) = self.local_file_manager.get_selected_file()
        # print(selected_row, selected_file)
        # selected_file.dump()

        selected_file_name = selected_file.name
        selected_file_loc_path = selected_file.relative_path
        self._log("File name <%s>, local path <%s>." % (selected_file_name, selected_file_loc_path))

        if selected_file_name != None:

            self.disable_control()
            self.temperature_active()

            self.printer_if.select_local_file(selected_file_loc_path)
            self.printer_if.start_print()

            self.pushbutton_sd_print.setEnabled(False)
            self.pushbutton_usb_print.setEnabled(False)
            self.pushbutton_loc_print.setEnabled(False)
            self.pushbutton_active_print.setEnabled(True)
            self.pushbutton_stop_print.setEnabled(True)

            # self.temp_pop.activeprint()
            # self.temp_pop.update_parameters()
            # self.temp_pop.ActivePrintWid.FileProgress.setValue(0)
            # control_page = self.ui_controller.get_page(k_control_page)
            # control_page.setEnabled(False)
            #self.parent.Control.setEnabled(False)

    def usb_start_print(self):
        self._log("UI: User touched (USB) Start Print")
        (selected_row, selected_file) = self.usb_file_manager.get_selected_file()

        selected_file_name = selected_file.name
        selected_file_rel = selected_file.relative_path
        selected_file_abs = selected_file.absolute_path
        self._log("File name <%s>, relative path <%s>, absolute path <%s>." % (selected_file_name, selected_file_rel, selected_file_abs))

        if selected_file_name != None:

            self.disable_control()
            self.temperature_active()

            wrapped_file = DiskFileWrapper(selected_file_name, selected_file_abs, False)
            self.local_storage_manager.add_file(selected_file_name, wrapped_file, allow_overwrite=True)

            self.printer_if.select_local_file(selected_file_name)
            self.printer_if.start_print()

            self.pushbutton_sd_print.setEnabled(False)
            self.pushbutton_usb_print.setEnabled(False)
            self.pushbutton_loc_print.setEnabled(False)
            self.pushbutton_active_print.setEnabled(True)
            self.pushbutton_stop_print.setEnabled(True)

            # self.temp_pop.activeprint()
            # self.temp_pop.update_parameters()
            # self.temp_pop.ActivePrintWid.FileProgress.setValue(0)
            # self.parent.Control.setEnabled(False)

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
        self._log("UI: User touched Active Print")
        self.ui_controller.push(k_temperature_page)
        # if self.fullscreen:
        #     self._log("UI: showing temp fullscreen")
        #     # self.temp_pop.showFullScreen()
        #     # self.close()
        # else:
        #     self._log("UI: showing temp")
        #     # self.temp_pop.show()
        #     # self.close()

    def update_loc_button_states_none(self):
        self.pushbutton_loc_up.setEnabled(False)
        self.pushbutton_loc_open.setEnabled(False)
        self.pushbutton_loc_print.setEnabled(False)

    def update_loc_button_states(self):
        selected_row, selected_file, selected_item = self.get_selected_loc_file()

        if self.loc_subdir.depth() > 0:
            self.pushbutton_loc_up.setEnabled(True)
        else:
            self.pushbutton_loc_up.setEnabled(False)

        if selected_row == -1:
            self.pushbutton_loc_open.setEnabled(False)
            self.pushbutton_loc_print.setEnabled(False)
            return

        if selected_file.type == 'd':
            self.pushbutton_loc_open.setEnabled(True)
            self.pushbutton_loc_print.setEnabled(False)

        elif selected_file.type == 'f':
            self.pushbutton_loc_open.setEnabled(False)
            self.pushbutton_loc_print.setEnabled(True)

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
