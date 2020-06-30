from builtins import str
import logging

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

from printer_if import PrinterIF
from .basepage import BasePage
from .qt.serialpage_qt import Ui_SerialPage
from .runout_handler import RunoutHandlerDialog

class SerialPage(BasePage, Ui_SerialPage):
    def __init__(self, context):
        super(SerialPage, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("SerialPage __init__()")

        # Set up the UI
        self.setupUi(self)
        self.printer_if = context.printer_if
        self.ui_controller = context.ui_controller

        ctor = self.printer_if.state_change_connector()
        ctor.register(self.state_change_callback)

        # self.event_handler = event_handler
        # self.event_handler.reconnect_serial.connect(self.reconnect_serial)

        # self.serial.data.checkserial_msg.connect(self.checkserial_msg)

        # Make the selection Behavior as selecting the entire row
        self.w_table_ports.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.w_table_ports.setSelectionMode(QtWidgets.QTableView.SingleSelection)

        # Hide the vertical header which contains the Index of the row.
        self.w_table_ports.verticalHeader().hide()

        # Stretch out the horizontal header to take up the entire view
        header = self.w_table_ports.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.scan_serial()
        # self.connect_serial()

        self.setbuttonstyle(self.w_pushbutton_back)

        self.w_pushbutton_back.clicked.connect(self.back)

        self.w_pushbutton_scan.clicked.connect(self.scan_serial)
        self.w_pushbutton_connect.clicked.connect(self.user_connect_serial)
        self.w_pushbutton_disconnect.clicked.connect(self.disconnect_serial)

        self.w_connect_popup = RunoutHandlerDialog(self, self.printer_if)
        self.w_disconnect_popup = RunoutHandlerDialog(self, self.printer_if)

        self.disconnect_expected = False

    def is_connection_transition_state(self, state):
        if state == "OPEN_SERIAL" or \
           state == "DETECT_SERIAL" or \
           state == "DETECT_BAUDRATE" or \
           state == "CONNECTING":
                return True
        return False

    def state_change_callback(self, from_state, to_state):
        self._log("**************** STATE CHANGE from %s to %s." % (from_state, to_state))

        # If we have transition from connecting state to any other
        # state, re-enable the page.
        if not self.is_connection_transition_state(to_state):
            self.enable_page()

        # Has a disconnect occurred?
#        if from_state == "OPERATIONAL" and to_state != "OPERATIONAL" and to_state != "ERROR":
        if from_state != "OFFLINE" and to_state == "OFFLINE":

            self._log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self._log("Disconnect detected!")

            # Disconnect occurred. Were we expecting it?
            if self.disconnect_expected:

                # We expected a disconnect, and now it's happened. Further
                # disconnects are unexpected
                self._log("Disconnect expected, resetting.")
                self.disconnect_expected = False

            else:

                # We are not expecting the disconnect. Pop up the
                # error dialog.
                self._log("Disconnect unexpected, popping up error dialog.")
                self.w_disconnect_popup.w_runout_title.setText("*** ERROR ***")
                self.w_disconnect_popup.w_runout_message_label.setText("Printer disconnected.")
                self.w_disconnect_popup.enable_ok()
                self.w_disconnect_popup.send_m108_on_ok = False
                self.w_disconnect_popup.hide_on_ok = True
                self.w_disconnect_popup.show()

        if to_state == "OPERATIONAL":
            self.disconnect_expected = False

        if to_state == "ERROR":
            self.disconnect_expected = True

        # If we have successfully connected, pop up a dialog.
        # if (from_state == "CONNECTING") and (to_state == "OPERATIONAL"):
        #     self.w_connect_popup.w_runout_title.setText("")
        #     self.w_connect_popup.w_runout_message_label.setText("Printer connected.")
        #     self.w_connect_popup.enable_ok()
        #     self.w_connect_popup.send_m108_on_ok = False
        #     self.w_connect_popup.hide_on_ok = True
        #     self.w_connect_popup.show()
            

    def _log(self, message):
        self._logger.debug(message)

    def reconnect_serial(self):
        if self.scan_serial():
            self.connect_serial()

    def checkserial_msg(self):
        # self.output_serial(self.serial.data.serial_msg)
        self.scan_serial()

    def output_serial(self, text):
        self.w_textb_output.moveCursor(QtGui.QTextCursor.End)
        self.w_textb_output.ensureCursorVisible()
        self.w_textb_output.append(text)

    def user_connect_serial(self):
        self._log("UI: User touched Connect")
        self.disable_page()
        self.connect_serial()

    def disable_page(self):
        self.w_pushbutton_scan.setEnabled(False)
        self.w_pushbutton_connect.setEnabled(False)
        self.w_pushbutton_disconnect.setEnabled(False)
        self.w_pushbutton_back.setEnabled(False)
        self.w_table_ports.setEnabled(False)

    def enable_page(self):
        self.w_pushbutton_scan.setEnabled(True)
        self.w_pushbutton_connect.setEnabled(True)
        self.w_pushbutton_disconnect.setEnabled(True)
        self.w_pushbutton_back.setEnabled(True)
        self.w_table_ports.setEnabled(True)

    def connect_serial(self):
        self._log("UI: User touched Connect")
        self.disconnect_expected = True
        selected_row = self.w_table_ports.currentRow()
        selected_device = self.w_table_ports.item(selected_row, 0).text()
        self._log("Connecting to device <%s>." % selected_device)
        self.printer_if.connect(selected_device)

    def disconnect_serial(self):
        self._log("UI: User touched Disconnect")
        # self.output_serial(self.serial.disconnect())
        self.disconnect_expected = True
        self.printer_if.disconnect()

    def scan_serial(self):
        self._log("UI: User touched Scan")
        # Call the printer to get its connection options
        serial_port_list = self.printer_if.get_connection_options()

        # Reset the port list UI
        self.w_table_ports.setRowCount(0)

        # Loop through the serial port options
        for p in serial_port_list:
        
            rowpos = self.w_table_ports.rowCount()

            self.w_table_ports.insertRow(rowpos)
            # device 
            device = QtWidgets.QTableWidgetItem(p)
            device.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            # descrip = QtWidgets.QTableWidgetItem("")
            # descrip.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            self.w_table_ports.setItem(rowpos, 0, device)
            # self.w_table_ports.setItem(rowpos, 1, descrip)

            if '/dev/ttyUSB' in p:
                self.w_table_ports.selectRow(rowpos)
                return True
