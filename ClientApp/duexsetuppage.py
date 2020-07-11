from qt.duexsetuppage_qt import Ui_DuExSetupPage
import logging
import re
import time
from PyQt5.QtCore import QObject, pyqtSignal
from basepage import BasePage
from numeric_keypad import NumericKeypad
from PyQt5 import QtWidgets

duex_regex = re.compile(
    "echo:Hotend offsets: ([-\\.0-9]+),([-\\.0-9]+) ([-\\.0-9]+),([-\\.0-9]+)", re.IGNORECASE)


class DuExSetupPage(BasePage, Ui_DuExSetupPage):

    info_signal = pyqtSignal(str)

    def __init__(self, context):
        super(DuExSetupPage, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("DuExSetupPage __init__()")

        # Keep a reference to the OctoPrint printer object and register to receive callbacks
        # from it.

        self.ui_controller = context.ui_controller
        self.printer_if = context.printer_if
        self.printer_if.set_duex_callback(self.duex_callback)

        # Set up user interface
        self.setupUi(self)

        # Set up callback functions
        self.w_pushbutton_temporary.clicked.connect(
            self.handle_temporary_touch)
        self.w_pushbutton_permanent.clicked.connect(
            self.handle_permanent_touch)
        self.w_pushbutton_revert.clicked.connect(self.handle_revert_touch)

        self.filter_output = False

        self.num_keys = NumericKeypad(self)
        self.num_keys.changed.connect(self.handle_change)
        self.num_keys.cleared.connect(self.handle_clear)

        self.focused_lineedit = None

        self.w_lineedit_x1.focus_in.connect(self.handle_x1_focus_in)
        self.w_lineedit_x1.focus_out.connect(self.handle_x1_focus_out)
        self.w_lineedit_y1.focus_in.connect(self.handle_y1_focus_in)
        self.w_lineedit_y1.focus_out.connect(self.handle_y1_focus_out)
        self.handle_x1_focus_in()
        self.handle_y1_focus_in()
        self.handle_x1_focus_out()
        self.handle_y1_focus_out()
        self.Back.clicked.connect(self.back)

        self.setStyleProperty(self.BottomBar, "bottom-bar")
        self.setStyleProperty(self.LeftBar, "left-bar")
        self.setAllStyleProperty(
            [self.w_lineedit_x1, self.w_lineedit_y1], "no-border")
        self.setAllTransparentButton([self.w_pushbutton_1, self.w_pushbutton_2, self.w_pushbutton_3,
                                      self.w_pushbutton_4, self.w_pushbutton_5, self.w_pushbutton_6,
                                      self.w_pushbutton_8, self.w_pushbutton_7, self.w_pushbutton_9,
                                      self.w_pushbutton_negative, self.w_pushbutton_0, self.w_pushbutton_decimal,
                                      self.w_pushbutton_delete, self.w_pushbutton_clear])
        self.setAllTransparentIcon([self.t1xIcon, self.t1yIcon])
        self.setAllTransparentButton([self.Back, self.w_pushbutton_permanent,
                                      self.w_pushbutton_temporary, self.w_pushbutton_revert], True)

    def just_pushed(self):
        self._log("just_pushed callback called!")
        self.get_settings()
        self.w_lineedit_x1.setFocus()

    def handle_x1_focus_in(self):
        self.num_keys.setEnabled(True)
        self.focused_lineedit = self.w_lineedit_x1
        self.num_keys.load(self.focused_lineedit.text())

    def handle_x1_focus_out(self):
        self.num_keys.setEnabled(False)
        self.focused_lineedit = self.w_lineedit_x1
        self.handle_focus_out()
        self.focused_lineedit = None

    def handle_y1_focus_in(self):
        self.num_keys.setEnabled(True)
        self.focused_lineedit = self.w_lineedit_y1
        self.num_keys.load(self.focused_lineedit.text())

    def handle_y1_focus_out(self):
        self.num_keys.setEnabled(False)
        self.focused_lineedit = self.w_lineedit_y1
        self.handle_focus_out()
        self.focused_lineedit = None

    def handle_change(self, value):
        if self.focused_lineedit is None:
            return

        self.focused_lineedit.setText(value)

    def handle_focus_out(self):
        # We need to look at the text in the focused LineEdit, to
        # ensure that its value makes sense as a number.
        value_str = self.focused_lineedit.text()

        if value_str == "" or value_str == "-" or value_str == "0.":
            value = 0.0
        else:
            value = float(value_str)

        value_str = "%0.4f" % value
        self.focused_lineedit.setText(value_str)

    def handle_clear(self, value):
        if self.focused_lineedit is None:
            self.w_lineedit_x1.setFocus()
            return

        self.focused_lineedit.setText("")
        self.num_keys.load("")

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


class DuexLineEdit(QtWidgets.QLineEdit):
    focus_in = pyqtSignal()
    focus_out = pyqtSignal()

    def __init__(self, parent):
        self.super = super(DuexLineEdit, self)
        self.super.__init__(parent)

    def focusInEvent(self, event):
        self.super.focusInEvent(event)
        self.focus_in.emit()

    def focusOutEvent(self, event):
        self.super.focusOutEvent(event)
        self.focus_out.emit()
