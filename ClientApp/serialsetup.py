from builtins import str
import logging

from PyQt5.QtCore import Qt

from .qt.serialwindow import *
from printer_if import PrinterIF

class SerialWindow(QtWidgets.QWidget, Ui_SerialWindow):
    def __init__(self, printer_if, event_handler, parent=None):
        super(SerialWindow, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("SerialWindow __init__()")

        # Set up the UI
        self.setupUi(self)
#        self.printer = printer
        self.printer_if = printer_if
        self.event_handler = event_handler
        self.event_handler.reconnect_serial.connect(self.reconnect_serial)
        # self.serial.data.checkserial_msg.connect(self.checkserial_msg)

        # Make the selection Behavior as selecting the entire row
        self.COMlist.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.COMlist.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        # Hide the vertical header which contains the Index of the row.
        self.COMlist.verticalHeader().hide()
        # Stretch out the horizontal header to take up the entire view
        header = self.COMlist.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.scan_serial()
        # self.connect_serial()

        self.Back.clicked.connect(self.user_back)
        self.ScanSerial.clicked.connect(self.scan_serial)
        self.ConnectSerial.clicked.connect(self.user_connect_serial)
        self.DisconnectSerial.clicked.connect(self.disconnect_serial)

    def _log(self, message):
        self._logger.debug(message)

    def user_back(self):
        self._log("UI: User touched Back")
        self.close()

    def reconnect_serial(self):
        if self.scan_serial():
            self.connect_serial()

    def checkserial_msg(self):
        # self.output_serial(self.serial.data.serial_msg)
        self.scan_serial()

    def output_serial(self, text):
        self.SerialOutput.moveCursor(QtGui.QTextCursor.End)
        self.SerialOutput.ensureCursorVisible()
        self.SerialOutput.append(text)

    def user_connect_serial(self):
        self._log("UI: User touched Connect")
        self.connect_serial()

    def connect_serial(self):
        selected_row = self.COMlist.currentRow()
        selected_device = self.COMlist.item(selected_row, 0).text()
        self._log("Connecting to device <%s>." % selected_device)
        self.printer_if.connect(selected_device)

    def disconnect_serial(self):
        self._log("UI: User touched Disconnect")
        # self.output_serial(self.serial.disconnect())
        self.printer_if.disconnect()

    def scan_serial(self):
        self._log("UI: User touched Scan")
        # Call the printer to get its connection options
        serial_port_list = self.printer_if.get_connection_options()

        # Reset the port list UI
        self.COMlist.setRowCount(0)

        # Loop through the serial port options
        for p in serial_port_list:
        
            rowpos = self.COMlist.rowCount()

            self.COMlist.insertRow(rowpos)
            # device 
            device = QtWidgets.QTableWidgetItem(p)
            device.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            descrip = QtWidgets.QTableWidgetItem("")
            descrip.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.COMlist.setItem(rowpos, 0, device)
            self.COMlist.setItem(rowpos, 1, descrip)

            if '/dev/ttyUSB' in p:
                self.COMlist.selectRow(rowpos)
                return True
