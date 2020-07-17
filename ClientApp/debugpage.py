import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from fsutils.tarballer import Tarballer
from util.log import find_root_logger
from .popup import PopUp

from basepage import BasePage
from touchscreen.qt.debugpage_qt import Ui_DebugPage


class DebugPage(BasePage, Ui_DebugPage):

    display_signal = pyqtSignal(str)

    def __init__(self, context):
        super(DebugPage, self).__init__()

        # Save context data
        self.printer_if = context.printer_if
        self.personality = context.personality
        self.ui_controller = context.ui_controller

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("DebugPage __init__()")

        # Set up user interface
        self.setupUi(self)

        # Set up callback functions
        self.w_pushbutton_add_marker.clicked.connect(self.handle_add_marker)
        self.w_pushbutton_copy_log.clicked.connect(self.handle_copy_log)
        self.w_pushbutton_send_fake_ack.clicked.connect(self.send_fake_ack)
        self.w_combobox_debuglevel.currentIndexChanged.connect(
            self.debug_level_changed)

        self.display_signal.connect(self.slot_display)
        self.Back.clicked.connect(self.back)

        self.setAllStyleProperty([self.logging_label], "white-transparent-text font-m align-center")

        self.setStyleProperty(self.BottomBar, "bottom-bar")
        self.setStyleProperty(self.LeftBar, "left-bar")
        self.setAllTransparentButton([self.Back, self.w_pushbutton_add_marker,
                                      self.w_pushbutton_copy_log, self.w_pushbutton_send_fake_ack], True)

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

        self.popup_signal.emit("", "New Logging Level: "+new_level_str, "", False)

    def handle_add_marker(self):
        self._log("UI: User touched Add Marker")

        message = self.w_lineedit_message.text()

        self._log(
            "******************************************************************************")
        self._log("* User log message <%s>" % message)
        self._log(
            "******************************************************************************")

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
