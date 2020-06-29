import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from .fsutils.subfilesystem import SubFileSystem


class FileListManager:

    def __init__(self, name, file_list_wid, watchpoint,
                 pathlabel_wid, pushbutton_up_wid,
                 pushbutton_open_wid, pushbutton_print_wid):

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("FileListManager __init__")

        self.name = name

        self.enabled = False

        self.pushbutton_up_wid = pushbutton_up_wid
        self.pushbutton_open_wid = pushbutton_open_wid
        self.pushbutton_print_wid = pushbutton_print_wid

        self.file_list_wid = file_list_wid
        self.watchpoint = watchpoint
        self.pathlabel_wid = pathlabel_wid

        self.item_stack = []

        self.file_list_wid.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows)
        self.file_list_wid.setSelectionMode(
            QtWidgets.QTableView.SingleSelection)
        self.file_list_wid.verticalHeader().hide()

        header = self.file_list_wid.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.file_list_wid.itemSelectionChanged.connect(self.itemClicked)
        self.file_list_wid.itemDoubleClicked.connect(self.itemDoubleClicked)

        self.pushbutton_open_wid.clicked.connect(self.open_subdir)
        self.pushbutton_up_wid.clicked.connect(self.up_dir)

        self.subdir = SubFileSystem(self.watchpoint)
        self.pathlabel_wid.setText(self.subdir.abspath)

        self.clear_files()
        self.update_button_states()

    def _log(self, message):
        self._logger.debug(message)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def update_files(self):
        self.file_list_wid.clearContents()
        self.file_list_wid.setRowCount(0)
        files = self.subdir.list()

        for file in files:

            rowpos = self.file_list_wid.rowCount()

            self.file_list_wid.insertRow(rowpos)

            file = QtWidgets.QTableWidgetItem(file.displayname)
            file.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            if file.type == 'f':
                size_str = str(file.size)
            else:
                size_str = ""

            size = QtWidgets.QTableWidgetItem(size_str)
            size.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.file_list_wid.setItem(rowpos, 0, file)
            self.file_list_wid.setItem(rowpos, 1, size)

    def clear_files(self):
        self.pathlabel_wid.setText("")
        self.file_list_wid.clearContents()
        self.file_list_wid.setRowCount(0)

    def get_selected_file(self):
        return self.get_selected_widget_file(self.file_list_wid, self.subdir)

    def get_selected_widget_file(self, list_widget, subdir):

        foolist = list_widget.selectedItems()

        if len(foolist) < 1:
            return (-1, None)

        selected_row = list_widget.currentRow()

        if selected_row == -1:
            return (-1, None, None)

        selected_file = subdir.files[selected_row]

        # selected_item = list_widget.currentItem()

        # selected_file_name = selected_file.name
        # selected_file_path = subdir.cwd + "/" + selected_file_name

        # return (selected_row, selected_file, selected_item, selected_file_path)
        return (selected_row, selected_file)

    def update_button_states_none(self):
        self.pushbutton_up_wid.setEnabled(False)
        self.pushbutton_open_wid.setEnabled(False)
        self.pushbutton_print_wid.setEnabled(False)

    def update_button_states(self):
        select_tuple = self.get_selected_file()

        selected_row, selected_file = select_tuple

        if self.subdir.depth() > 0:
            self.pushbutton_up_wid.setEnabled(True)
        else:
            self.pushbutton_up_wid.setEnabled(False)

        if selected_row == -1:
            self.pushbutton_open_wid.setEnabled(False)
            self.pushbutton_print_wid.setEnabled(False)
            return

        if selected_file.type == 'd':
            self.pushbutton_open_wid.setEnabled(True)
            self.pushbutton_print_wid.setEnabled(False)

        elif selected_file.type == 'f':
            self.pushbutton_open_wid.setEnabled(False)
            self.pushbutton_print_wid.setEnabled(True)

    def itemClicked(self):
        self._log("UI: User touched item")
        row = self.file_list_wid.currentRow()
        self.update_button_states()

    def itemDoubleClicked(self):
        self.open_subdir()

    def open_subdir(self):
        if not self.enabled:
            return
        self._log("UI: User touched Open")
        (selected_row, selected_file) = self.get_selected_file()

        if selected_row is None:
            return

        if selected_file.type != 'd':
            return

        self.item_stack.append(selected_row)

        self.subdir.cd(selected_file.name)
        self.update_files()
        self.showFileAndDeselect(0)
        self.update_button_states()
        self.pathlabel_wid.setText(self.subdir.abspath)

    def up_dir(self):
        if not self.enabled:
            return
        self._log("UI: User touched Up")
        self.subdir.up()
        self.update_files()

        selected_row = self.item_stack.pop()
        self.showFile(selected_row)

        self.update_button_states()
        self.pathlabel_wid.setText(self.subdir.abspath)

    def showFile(self, selected_row):
        self.file_list_wid.setCurrentCell(selected_row, 0)
        selected_item = self.file_list_wid.currentItem()
        self.file_list_wid.scrollToItem(selected_item)

    def showFileAndDeselect(self, selected_row):
        self.file_list_wid.setCurrentCell(selected_row, 0)
        selected_item = self.file_list_wid.currentItem()
        self.file_list_wid.scrollToItem(selected_item)
        self.file_list_wid.setCurrentItem(None)

    def update_create(self, path):
        self.pathlabel_wid.setText(path)
        self.subdir = SubFileSystem(path)
        self.update_files()
        self.update_button_states()
