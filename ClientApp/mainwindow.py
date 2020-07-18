import logging
import re

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QWidget, QLabel

from .qt.mainwindow_qt import Ui_MainWindow

from constants import Pages
from context import Context

from .basepage import BasePage
from .homepage import HomePage
from .printpage import PrintPage
from .controlpage import ControlPage
from .temperaturepage import TemperaturePage
from .settingspage import SettingsPage
from .debugpage import DebugPage
from .infopage import InfoPage
from .serialpage import SerialPage
from .userupdatepage import UserUpdatePage
from .duexsetuppage import DuExSetupPage
from .popup import PopUp
from .runout import RunOut
from .notification import Notification


class MainWindow(BasePage, Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, printer_if, persona, properties):
        super(MainWindow, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("MainWindow starting up")

        self.context = Context(printer_if, persona, self, properties)
        self.printer_if = printer_if

        # Initialize the UI
        self.setupUi(self)

        # Setup the home page
        self.home_page = HomePage(self.context)
        self.stack.addWidget(self.home_page)

        self.pages = {}
        context = self.context

        # Create the various other pages
        self.add_page(self.home_page, Pages.HOME_PAGE)
        self.add_page(PrintPage(context), Pages.PRINT_PAGE)
        self.add_page(ControlPage(context), Pages.CONTROL_PAGE)
        self.add_page(TemperaturePage(context), Pages.TEMPERATURE_PAGE)
        self.add_page(SettingsPage(context), Pages.SETTINGS_PAGE)
        self.add_page(DebugPage(context), Pages.DEBUG_PAGE)
        self.add_page(InfoPage(context), Pages.INFO_PAGE)
        self.add_page(SerialPage(context), Pages.SERIAL_PAGE)
        self.add_page(UserUpdatePage(context), Pages.USERUPDATE_PAGE)
        self.add_page(DuExSetupPage(context), Pages.DUEXSETUP_PAGE)

        #Create one popup instance that is shown when the signal is emited from a page. 
        self.popup = PopUp(self)
        #Connect the each popup_signal to a singular function. 
        self.popup_signal.connect(self.show_popup)
        for p in self.pages:
            self.pages[p].popup_signal.connect(self.show_popup) 


        # Start the UI on the Home page
        self.stack.setCurrentWidget(self.home_page)

        # Create the data structure that will contain the stack of
        # pages to display.
        self.page_stack = []

        # Activate the window to take keyboard focus.
        self.setWindowState(Qt.WindowActive)
        self.activateWindow()

        self.printer_if.set_state_changed_callback(self.state_changed_callback)
        self.w_runout_handler = RunOut(self, self.printer_if)
        self.printer_if.set_runout_callback(self.w_runout_handler)

        ctor = self.printer_if.state_change_connector()
        ctor.register(self.state_change_connector_callback)

        self.setStyleProperty(self.status, "bottom-bar")
        self.setAllStyleProperty(
            [self.right_status, self.left_status, self.middle_status], "white-transparent-text")

    prog = re.compile("Heater_ID: ([^ ]+)")

    def state_change_connector_callback(self, from_state, to_state):
        if to_state.startswith("ERROR"):
            state_string = self.printer_if.get_printer().get_state_string()
            self._log(
                "################################################################################################")
            self._log("from state <%s> to state <%s>" % (from_state, to_state))
            self._log("state string <%s>" % state_string)

            message_string = ""
            detail_string = "Message from printer:\n%s" % state_string

            result = self.prog.search(state_string)

            if result is not None:
                id = result.group(1)
                if id == "bed":
                    message_string = "Printer bed failed to heat.\n"
                else:
                    message_string = "Extruder %s failed to heat.\n" % id

            # This is the default message.
            message_string += "Printer halted."

            self.popup_signal.emit("*** ERROR ***", message_string, detail_string, False)
 
    def state_changed_callback(self, payload):
        state = "Printer: %s" % payload["state_string"]
        self._log("NEW PRINTER STATE " + state)
        self.set_middle_status(state)

    def list_children(self, widget):
        children = widget.findChildren(QObject, "")
        for child in children:
            print("Child", child)

    def add_page(self, page, page_name):
        self.stack.addWidget(page)
        self.pages[page_name] = page
        return page

    def get_page(self, page_name):
        try:
            widget = self.pages[page_name]
            return widget
        except KeyError:
            return None

    def _log(self, message):
        self._logger.debug(message)

    def set_left_status(self, text):
        self.left_status.setText(text)

    def set_middle_status(self, text):
        self.middle_status.setText(text)

    def set_right_status(self, text):
        self.right_status.setText(text)

    def push(self, page_name):
        try:
            # Get the page we're going to display next.
            widget = self.pages[page_name]

            # Get the current paget being display and push it onto
            # the page stack so we can pop back to it later.
            self.page_stack.append(self.stack.currentWidget())

            # Display the next page
            self.stack.setCurrentWidget(widget)

            # Call the page's "just_pushed" method, if it exists. This
            # callback enables pages to perform processing after being
            # pushed, such as focusing a particular widget.

            just_pushed_op = getattr(widget, "just_pushed", None)

            if callable(just_pushed_op):
                self._log(
                    "<%s> just_pushed callback exists, calling..." % page_name)
                widget.just_pushed()

        except KeyError:
            # If the name of the requested widget to push doesn't
            # exist, log an error.
            self._log("MainWindow: page \"%s\" not found." % page_name)

    def pop(self):
        try:
            # Pop the previously pushed widget...
            widget = self.page_stack.pop()

            # ...And display it.
            self.stack.setCurrentWidget(widget)

        except IndexError:
            # An index error indicates we tried to pop when the stack
            # was empty.
            self._log("ERROR: popping from an empty stack!")

    def show_popup(self, title, mess, dets, hideButton = False):
        self.popup.popup_title.setText(title)
        self.popup.popup_message.setText(mess)
        self.popup.popup_details.setText(dets)
        if(hideButton): self.popup.popup_button.setVisible(False)
        self.popup.show()