from __future__ import division
from builtins import str
from constants import Pages

import logging

from past.utils import old_div
from PyQt5 import QtCore, QtGui, QtWidgets, QtQuickWidgets, QtQuick
from PyQt5.QtCore import Qt, pyqtSignal

from octoprint.filemanager import storage
from octoprint.filemanager.util import DiskFileWrapper

from qt.printpage_qt import *
from fsutils.subfilesystem import *
from fsutils.file import *
from fsutils.mountpoint import MountPoint
from fsutils.filelistmanager import FileListManager
from basepage import BasePage
from model.tablemodel import TableModel


class PrintPage(BasePage, Ui_PrintPage):

    # Create the Qt signals we're going to use for updating the list
    # of USB files. Each signal takes a single argument, which is the
    # path to the newly mounted (created) or unmounted (deleted)
    # directory.
    sdfile_signal = pyqtSignal(list)

    SDrowClickedSignal = pyqtSignal(int)
    USBrowClickedSignal = pyqtSignal(int)
    LocalrowClickedSignal = pyqtSignal(int)

    def __init__(self, context):
        super(PrintPage, self).__init__()

        self.printer_if = context.printer_if
        self.personality = context.personality
        self.ui_controller = context.ui_controller

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log_d("PrintPage __init__")

        # Connect slots to the signals
        self.sdfile_signal.connect(self.update_sd_files)

        # Set up the rest of the UI
        self.setupUi(self)

        self.printer_if.set_file_list_update_callback(
            self.sd_file_list_update_callback)
        # print("Setting print finished callback")
        self.printer_if.set_print_finished_callback(self.print_finished_callback)

        self.item_stack = []

        self.pushbutton_scan_sd.clicked.connect(self.scansd)
        self.pushbutton_start_print.clicked.connect(self.sd_start_print)
        self.pushbutton_start_print.clicked.connect(self.local_start_print)
        self.pushbutton_start_print.clicked.connect(self.usb_start_print)

        self.pushbutton_active_print.clicked.connect(self.activeprintpop)
        self.pushbutton_stop_print.clicked.connect(self.stopprint)

        self.pushbutton_active_print.setEnabled(False)
        self.pushbutton_stop_print.setEnabled(False)

        #SETUP SD QML TABLE
        self.SDTableModel = TableModel(self, ["Name", "Size"], [7,3], rowClickedSignal = self.SDrowClickedSignal)
        self.SDTable = self.setUpQMLTable(self.SDMainLayout, self.SDTableModel)
        self.SDTableLayout.addWidget(self.SDTable)
        self.SDrowClickedSignal.connect(self.sd_rowClicked)
        self.sd_selectedRow = -1

        #SETUP USB QML TABLE
        self.USBTableModel = TableModel(self, ["Name", "Size"], [7,3], rowClickedSignal = self.USBrowClickedSignal)
        self.USBTable = self.setUpQMLTable(self.USBMainLayout, self.USBTableModel)
        self.USBTableLayout.addWidget(self.USBTable)

        #SETUP USB QML TABLE
        self.LocalTableModel = TableModel(self, ["Name", "Size"], [7,3], rowClickedSignal = self.LocalrowClickedSignal)
        self.LocalTable = self.setUpQMLTable(self.LocalMainLayout, self.LocalTableModel)
        self.LocalTableLayout.addWidget(self.LocalTable)

        # Set up the list of USB files
        self.usb_file_manager = FileListManager("USB", self.printer_if,
                                                self.USBTableModel, self.USBTable,
                                                self.personality.watchpoint,
                                                self.usb_pathlabel,
                                                self.pushbutton_folder_up,
                                                self.pushbutton_folder_open,
                                                self.pushbutton_start_print)

        # Set up the list of local files
        self.local_file_manager = FileListManager("Local", self.printer_if,
                                                  self.LocalTableModel, self.LocalTable,
                                                  self.personality.localpath,
                                                  self.loc_pathlabel,
                                                  self.pushbutton_folder_up,
                                                  self.pushbutton_folder_open,
                                                  self.pushbutton_start_print)

        self.local_file_manager.update_files()

        self.Back.clicked.connect(self.back)
        self.pushbutton_SDtab.clicked.connect(self.setSDtab)
        self.pushbutton_USBtab.clicked.connect(self.setUSBtab)
        self.pushbutton_Localtab.clicked.connect(self.setLocaltab)
        self.ButtonTabs = {"LOCAL":self.pushbutton_Localtab, "USB":self.pushbutton_USBtab, "SD": self.pushbutton_SDtab}

        self.print_method = ""
        self.setSDtab()
        self.file_being_printed = "-----"

        self.setAllTransparentButton([self.Back, self.pushbutton_active_print, self.pushbutton_start_print, self.pushbutton_stop_print,
                                      self.pushbutton_SDtab, self.pushbutton_USBtab, self.pushbutton_Localtab,
                                      self.pushbutton_scan_sd, self.pushbutton_folder_open, self.pushbutton_folder_up], True)
        self.setStyleProperty(self.BottomBar, "bottom-bar")
        self.setStyleProperty(self.LeftBar, "left-bar")
        self.setAllStyleProperty([self.sd_pathlabel, self.usb_pathlabel, self.loc_pathlabel,
                                    self.USB_Label, self.Local_Label], "black-transparent-text font-s")
        # self.setAllStyleProperty(
        #     [self.SDFileList, self.USBFileList, self.LocalFileList], "table-mode-1")



    def setUpQMLTable(self, layout, model):
        qmltable = QtQuickWidgets.QQuickWidget(layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(qmltable.sizePolicy().hasHeightForWidth())
        qmltable.setSizePolicy(sizePolicy)
        qmltable.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        qmltable.rootContext().setContextProperty("tableModel", model)
        qmltable.setSource(QtCore.QUrl("qrc:/qml/table.qml"))
        return qmltable

    def setSDtab(self):
        self.changeTabTo("SD")
        self.usb_file_manager.disable()
        self.local_file_manager.disable()
        self.stackedPrintingOptions.setCurrentIndex(0)
        self.showSDButtons(True)

    def setUSBtab(self):
        self.changeTabTo("USB")
        self.usb_file_manager.enable()
        self.local_file_manager.disable()
        self.stackedPrintingOptions.setCurrentIndex(1)
        self.usb_file_manager.update_button_states()
        self.showSDButtons(False)

    def setLocaltab(self):
        self.changeTabTo("LOCAL")
        self.usb_file_manager.disable()
        self.local_file_manager.enable()
        self.stackedPrintingOptions.setCurrentIndex(2)
        self.local_file_manager.update_button_states()
        self.showSDButtons(False)

    def changeTabTo(self, selectedTab):
        self.print_method = selectedTab
        for tab in self.ButtonTabs:
            if tab == selectedTab:
                self.ButtonTabs[tab].setIcon(QtGui.QIcon(QtGui.QPixmap((":/img/img/"+tab+".png"))))
            else:
                self.ButtonTabs[tab].setIcon(QtGui.QIcon(QtGui.QPixmap(QtGui.QPixmap(":/img/img/"+tab+"_2.png"))))

    def showSDButtons(self, isSDprinting):
        #Disable SD scan button if already printing
        self.pushbutton_scan_sd.setVisible(isSDprinting)
        self.pushbutton_folder_up.setVisible(not isSDprinting)
        self.pushbutton_folder_open.setVisible(not isSDprinting)

    def set_control_page(self, on):
        home_page = self.ui_controller.get_page(Pages.HOME_PAGE)
        home_page.pushbutton_control.setEnabled(on)

    def set_storage_manager(self, local_storage_manager):
        self.local_storage_manager = local_storage_manager

    def set_usb_mount_signals(self, tuple):
        (create_signal, delete_signal) = tuple
        create_signal.connect(self.update_usb_create)
        delete_signal.connect(self.update_usb_delete)

    def set_usb_content_signal(self, signal):
        signal.connect(self.update_usb_content)

    def set_local_content_signal(self, signal):
        signal.connect(self.update_local_content)

    def update_usb_create(self, mountpoint):
        self._log_d("UPDATE_USB_CREATE: path <%s>, actual path <%s>" %
                  (mountpoint.path, mountpoint.actual_path))
        self.usb_file_manager.update_create(mountpoint.path)

    def update_usb_delete(self, path):
        self.usb_file_manager.clear_files()

    def update_usb_content(self, path):
        self.usb_file_manager.update_files()

    def update_local_content(self, path):
        self.local_file_manager.update_files()


    def stopprint(self):
        self._log_d("UI: User touched Stop Print")
        self.printer_if.cancel_printing()
        self.print_finished_callback()

    def print_finished_callback(self):
        # self.temp_pop.notactiveprint()
        self.file_being_printed = "-----"
        temperature_page = self.ui_controller.get_page(Pages.TEMPERATURE_PAGE)
        temperature_page.notactiveprint()
        self.pushbutton_active_print.setEnabled(False)
        self.pushbutton_stop_print.setEnabled(False)
        self.pushbutton_start_print.setEnabled(True)
        self.pushbutton_scan_sd.setEnabled(True)
        self.printer_if.printing = False
        self.set_control_page(True)

    def temperature_active(self):
        temperature_page = self.ui_controller.get_page(Pages.TEMPERATURE_PAGE)
        temperature_page.activeprint()
        self._log_d("temperature_active: calling reset_parameters.")
        temperature_page.reset_parameters()
        temperature_page.set_progress(0)

    def temperature_inactive(self):
        temperature_page = self.ui_controller.get_page(Pages.TEMPERATURE_PAGE)
        temperature_page.notactiveprint()
        temperature_page.reset_parameters()
        temperature_page.set_progress(0)

    def activeprintpop(self):
        self._log_d("UI: User touched Active Print")
        self.ui_controller.push(Pages.TEMPERATURE_PAGE)

    def scansd(self):
        self._log_d("UI: User touched Scan")
        self.printer_if.release_sd_card()
        self.printer_if.init_sd_card()
        self.printer_if.list_sd_card()

    def sd_file_list_update_callback(self, sd_file_list):
        self.sdfile_signal.emit(sd_file_list)

    def update_sd_files(self, file_list):
        self.SDTableModel.updateDataList(file_list)
        self.SDTableModel.layoutChanged.emit()
        self.sd_selectedFile = None
        self.sd_selectedRow = -1
        self.SDTable.rootObject().findChild(QtCore.QObject, "tableView").setProperty("selectedRow", -1)

        self.pushbutton_start_print.setEnabled(False)


    def sd_rowClicked(self, row):
        self.sd_selectedRow = row
        self.sd_selectedFile = self.SDTableModel.get(self.sd_selectedRow, 0)
        if self.print_method == "SD" and not self.printer_if.printing:
            self.pushbutton_start_print.setEnabled(True)
        

    def sd_start_print(self):
        if not self.print_method == "SD":
            return
        self._log_d("UI: User touched (SD) Start Print")

        selected_file = self.sd_selectedFile

        # print("Printing <%s>" %(selected_file))
        if selected_file != None:
            self.file_being_printed = selected_file
            print("SD start print")

            self.temperature_active()
            self.set_control_page(False)

            self.printer_if.select_sd_file(selected_file)
            self.printer_if.start_print()

            self.pushbutton_start_print.setEnabled(False)
            self.pushbutton_active_print.setEnabled(True)
            self.pushbutton_stop_print.setEnabled(True)
            self.pushbutton_scan_sd.setEnabled(False)

    def local_start_print(self):
        if not self.print_method == "LOCAL":
            return
        self._log_d("UI: User touched (Local) Start Print")
        selected_file = self.usb_file_manager.selectedFile

        selected_file_name = selected_file.name
        selected_file_loc_path = selected_file.relative_path
        self._log_d("File name <%s>, local path <%s>." %
                  (selected_file_name, selected_file_loc_path))

        if selected_file_name != None:
            print("Local start print")
            self.file_being_printed = selected_file_name

            self.set_control_page(False)
            self.temperature_active()

            self.printer_if.select_local_file(selected_file_loc_path)
            self.printer_if.start_print()

            self.pushbutton_start_print.setEnabled(False)
            self.pushbutton_active_print.setEnabled(True)
            self.pushbutton_stop_print.setEnabled(True)
            self.pushbutton_scan_sd.setEnabled(False)

    def usb_start_print(self):
        if not self.print_method == "USB":
            return
        self._log_d("UI: User touched (USB) Start Print")
        selected_file = self.usb_file_manager.selectedFile

        selected_file_name = selected_file.name
        selected_file_rel = selected_file.relative_path
        selected_file_abs = selected_file.absolute_path
        self._log_d("File name <%s>, relative path <%s>, absolute path <%s>." % (
            selected_file_name, selected_file_rel, selected_file_abs))

        if selected_file_name != None:
            self.file_being_printed = selected_file_name

            self.set_control_page(False)
            self.temperature_active()

            wrapped_file = DiskFileWrapper(
                selected_file_name, selected_file_abs, False)
            self.local_storage_manager.add_file(
                selected_file_name, wrapped_file, allow_overwrite=True)

            self.printer_if.select_local_file(selected_file_name)
            self.printer_if.start_print()

            self.pushbutton_start_print.setEnabled(False)
            self.pushbutton_active_print.setEnabled(True)
            self.pushbutton_stop_print.setEnabled(True)
            self.pushbutton_scan_sd.setEnabled(False)

