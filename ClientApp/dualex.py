import logging
import re
import time

from PyQt5.QtCore import QObject, pyqtSignal

from .basewindow import BaseWindow
from qt.duexsetupwindow import *

duex_regex = re.compile("echo:Hotend offsets: ([\\.0-9]+),([\\.0-9]+) ([\\.0-9]+),([\\.0-9]+)", re.IGNORECASE)

class DuExSetupWindow(BaseWindow, Ui_duexSetupWindow):

    info_signal = pyqtSignal(str)

    def __init__(self, printer_if, parent=None):
        super(DuExSetupWindow, self).__init__(parent)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("DuExSetupWindow __init__()")

        # Keep a reference to the OctoPrint printer object and register to receive callbacks
        # from it.
        self.printer_if = printer_if
        self.printer_if.set_duex_callback(self.duex_callback)

        # Set up user interface
        self.setupUi(self)
        self.parent = parent

        # Set up callback functions
        self.w_pushbutton_temporary.clicked.connect(self.handle_temporary_touch)
        self.w_pushbutton_permanent.clicked.connect(self.handle_permanent_touch)
        self.w_pushbutton_revert.clicked.connect(self.handle_revert_touch)
        self.Back.clicked.connect(self.back)
        # self.info_signal.connect(self.info_do_it)

        self.filter_output = False

    def get_settings(self):
        self._log("Dual Extruder window getting current settings...")
        self.filter_output = True
        self.printer_if.commands("M218 T1")

    def handle_temporary_touch(self):
        self._log("UI: User touched Use Temporarily.")
        self.set_offsets_temporarily()

    def handle_permanent_touch(self):
        self._log("UI: User touched Make Permanent.")
        self.set_offsets_permanently()

    def handle_revert_touch(self):
        self._log("UI: User touched Revert.")
        self.printer_if.restore_settings()
        time.sleep(1.0)
        self.get_settings()

    def set_offsets_temporarily(self):
        x1 = self.w_lineedit_x1.text()
        y1 = self.w_lineedit_y1.text()

        command = "M218 T1 X%s Y%s" % (x1, y1)
        self._log("Setting offsets: <%s>" % command)

        self.printer_if.commands(command)

    def set_offsets_permanently(self):
        self.set_offsets_temporarily()
        self.printer_if.save_settings()
        time.sleep(1.0)
        self.get_settings()

    def duex_callback(self, data):

        if self.filter_output:

            if data == "ok":
                self.filter_output = False
                return

            if not data.startswith("echo:Hotend offsets:"):
                return

            match = duex_regex.match(data)

            if match:
                groups = match.groups()

                if len(groups) < 4:
                    self.w_lineedit_x1.setText("****")
                    self.w_lineedit_y1.setText("****")
                    return

                (x0, y0, x1, y1) = groups

                self.w_lineedit_x1.setText(x1)
                self.w_lineedit_y1.setText(y1)
