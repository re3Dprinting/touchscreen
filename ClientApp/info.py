import logging

from PyQt5.QtCore import QObject, pyqtSignal

from .basewindow import BaseWindow
from qt.infowindow import *

class InfoWindow(BaseWindow, Ui_InfoWindow):

    info_signal = pyqtSignal(str)

    def __init__(self, printer_if, parent=None):
        super(InfoWindow, self).__init__(parent)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("InfoWindow __init__()")

        # Keep a reference to the OctoPrint printer object and register to receive callbacks
        # from it.
        self.printer_if = printer_if
        self.printer_if.set_info_callback(self.info_callback)
        # printer = self.printer_if.get_printer().register_callback(self)

        # Set up user interface
        self.setupUi(self)
        self.parent = parent
        self.w_message_text.setReadOnly(True)

        # Set up callback functions
        self.w_pushbutton_info.clicked.connect(self.handle_info_touch)
        self.w_pushbutton_stats.clicked.connect(self.s_stats)
        self.Back.clicked.connect(self.back)
        self.info_signal.connect(self.info_do_it)

    # This is called externally from the Printer thread. We need to go
    # through a Qt signal for thread safety.

    def info_callback(self, data):

        # Emit the signal with the callback data.
        self.info_signal.emit(data)

    # Receive the signal bearing string data from the Printer thread.
    def info_do_it(self, data):

        # Simply display the data
        self.display(data)

    def handle_info_touch(self):
        self._log("UI: User touched Info")
        self.w_message_text.clear()
        self.printer_if.commands("M115")

    def s_stats(self):
        self._log("UI: User touched Stats")
        self.w_message_text.clear()
        self.printer_if.commands("M78")

    # Display a line on the screen
    def display(self, message):
        self.w_message_text.moveCursor(QtGui.QTextCursor.End)
        self.w_message_text.append(message)

