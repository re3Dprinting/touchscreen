import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from .subfilesystem import SubFileSystem


class FileListManager:

    def __init__(self, name, table_model, qmltable, watchpoint,
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

        #Elements for QML model/ table.
        self.table_model = table_model
        self.qmltable = qmltable


        self.watchpoint = watchpoint
        self.pathlabel_wid = pathlabel_wid

        self.item_stack = []

        self.table_model.rowClickedSignal.connect(self.rowClicked)
        self.selectedRow = -1

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
        files = self.subdir.list()
        self.table_model.updateDataList(files)
        self.table_model.layoutChanged.emit()

        # self.file_list_wid.clearContents()
        # self.file_list_wid.setRowCount(0)
        # for file in files:
        #     rowpos = self.file_list_wid.rowCount()

        #     self.file_list_wid.insertRow(rowpos)

        #     file = QtWidgets.QTableWidgetItem(file.displayname)
        #     file.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        #     if file.type == 'f':
        #         size_str = str(file.size)
        #     else:
        #         size_str = ""

        #     size = QtWidgets.QTableWidgetItem(size_str)
        #     size.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        #     self.file_list_wid.setItem(rowpos, 0, file)
        #     self.file_list_wid.setItem(rowpos, 1, size)

    def clear_files(self):
        self.pathlabel_wid.setText("")
        self.table_model.updateDataList([])
        self.table_model.layoutChanged.emit()
        # self.file_list_wid.clearContents()
        # self.file_list_wid.setRowCount(0)

    # def get_selected_file(self):
    #     return self.get_selected_widget_file(self.file_list_wid, self.subdir)

    # def get_selected_widget_file(self, list_widget, subdir):

    #     # foolist = list_widget.selectedItems()
        
    #     # if len(foolist) < 1:
    #     #     return (-1, None)

    #     # selected_row = list_widget.currentRow()

    #     # if selected_row == -1:
    #     #     return (-1, None, None)

    #     return( row, )

    #     selected_file = subdir.files[selected_row]

    #     return (selected_row, selected_file)

    def update_button_states_none(self):
        self.pushbutton_up_wid.setEnabled(False)
        self.pushbutton_open_wid.setEnabled(False)
        self.pushbutton_print_wid.setEnabled(False)

    def update_button_states(self):

        #Enabled up directory if we are in subdirectory
        if self.subdir.depth() > 0:
            self.pushbutton_up_wid.setEnabled(True)
        else:
            self.pushbutton_up_wid.setEnabled(False)
        #Nothing is Selected.
        if self.selectedRow == -1:
            self.pushbutton_open_wid.setEnabled(False)
            self.pushbutton_print_wid.setEnabled(False)
            return

        if self.selectedFile.type == 'd':
            self.pushbutton_open_wid.setEnabled(True)
            self.pushbutton_print_wid.setEnabled(False)

        elif self.selectedFile.type == 'f':
            self.pushbutton_open_wid.setEnabled(False)
            self.pushbutton_print_wid.setEnabled(True)

    def rowClicked(self, row):
        self._log("UI: User touched item")
        self.selectedRow = row
        self.selectedFile = self.table_model.getDataList()[self.selectedRow]
        self.update_button_states()


    def open_subdir(self):
        if not self.enabled:
            return
        self._log("UI: User touched Open")
        # (selected_row, selected_file) = self.get_selected_file()

        if self.selectedRow == -1:
            return

        if self.selectedFile.type != 'd':
            return

        self.item_stack.append(self.selectedRow)

        self.subdir.cd(self.selectedFile.name)
        self.update_files()

        #Deselect the row
        self.setSelectedRow(-1)
        self.update_button_states()
        self.pathlabel_wid.setText(self.subdir.abspath)

    def up_dir(self):
        if not self.enabled:
            return
        self._log("UI: User touched Up")
        self.subdir.up()
        self.update_files()

        #Scroll to previous selected file
        selected_row = self.item_stack.pop()
        # self.showFile(selected_row)
        self.setSelectedRow(selected_row)
        self.update_button_states()
        self.pathlabel_wid.setText(self.subdir.abspath)

    #Called when the printpage recieved a signal the a USB path is mounted. 
    def update_create(self, path):
        self.pathlabel_wid.setText(path)
        self.subdir = SubFileSystem(path)
        self.update_files()
        self.update_button_states()

    def setSelectedRow(self, row):
        self.selectedRow = row
        self.selectedFile = None if (row == -1) else self.table_model.getDataList()[self.selectedRow]
        self.qmltable.rootObject().findChild(QtCore.QObject, "tableView").setProperty("selectedRow", row)

    def showFile(self, selected_row):
        self.file_list_wid.setCurrentCell(selected_row, 0)
        selected_item = self.file_list_wid.currentItem()
        self.file_list_wid.scrollToItem(selected_item)

    def showFileAndDeselect(self, selected_row):
        self.file_list_wid.setCurrentCell(selected_row, 0)
        selected_item = self.file_list_wid.currentItem()
        self.file_list_wid.scrollToItem(selected_item)
        self.file_list_wid.setCurrentItem(None)
