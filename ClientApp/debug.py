import logging

from PyQt5.QtCore import pyqtSignal

from qt.debugwindow import *
from basewindow import BaseWindow
from fsutils.tarballer import Tarballer
from util.log import find_root_logger
from .runout_handler import RunoutHandlerDialog

from touchscreen.qt.debugwindow import Ui_DebugWindow


class DebugWindow(BaseWindow, Ui_DebugWindow):

    display_signal = pyqtSignal(str)
    
    def __init__(self, printer_if, personality, parent=None):
        super(DebugWindow, self).__init__(parent)

        # Save reference to printer interface
        self.printer_if = printer_if

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("DebugWindow __init__()")

        # Savepersonality
        self.personality = personality

        # Set up user interface
        self.setupUi(self)
        self.parent = parent

        # Set up callback functions
        self.w_pushbutton_add_marker.clicked.connect(self.handle_add_marker)
        self.w_pushbutton_copy_log.clicked.connect(self.handle_copy_log)
        self.w_pushbutton_send_fake_ack.clicked.connect(self.send_fake_ack)
        self.Back.clicked.connect(self.back)
        self.w_combobox_debuglevel.currentIndexChanged.connect(self.debug_level_changed)
        self.display_signal.connect(self.slot_display)

        self.w_runout_handler = RunoutHandlerDialog(self, self.printer_if)

    def signal_display(self, str):
        self.display_signal.emit(str)

    def slot_display(self, str):
        self.display(str)

    def debug_level_changed(self):
        print("### LEVEL CHANGED ###")
        new_index = self.w_combobox_debuglevel.currentIndex()
        print("New index = %d" % new_index)
        root_logger = find_root_logger()
        print("Root logger =", root_logger)

        if new_index == 0:
            root_logger.setLevel(logging.DEBUG)
            new_level_str = "DEBUG"
            self._log("Set debug level to DEBUG")

        if new_index == 1:
            self._log("Set debug level to INFO")
            new_level_str = "INFO"
            root_logger.setLevel(logging.INFO)

        self.w_runout_handler.w_runout_message_label.setText("New logging level = " + new_level_str)
        self.w_runout_handler.enable_ok()
        self.w_runout_handler.send_m108_on_ok = False
        self.w_runout_handler.hide_on_ok = True
        self.w_runout_handler.show()

    def handle_add_marker(self):
        self._log("UI: User touched Add Marker")

        message = self.w_lineedit_message.text()

        self._log("******************************************************************************")
        self._log("* User log message <%s>" % message)
        self._log("******************************************************************************")

        self.display("Log marker added.")

    # Send a fake acknowledgement
    def send_fake_ack(self):
        self._log("Sending fake acknowledgement.")
        self.printer_if.send_fake_ack()
        self.display("Sent fake acknowledgement.")

    # Display a line on the screen
    def display(self, message):
        self.w_message_text.moveCursor(QtGui.QTextCursor.End)
        self.w_message_text.append(message)

    def on_printer_add_message(self, data):
        print("GOT <%s>" % data)

    def handle_copy_log(self):
        tarballer = Tarballer(self, self.personality)
        tarballer.do_copy_log()
