import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QWidget, QLabel

from .qt.mainwindow_qt import Ui_MainWindow

from constants import *
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


class MainWindow(BasePage, Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, printer_if, persona, properties):
        super(MainWindow, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("MainWindow starting up")

        self.context = Context(printer_if, persona, self, properties)

        # Initialize the UI
        self.setupUi(self)

        # Setup the home page
        self.home_page = HomePage(self.context)
        self.stack.addWidget(self.home_page)

        self.pages = {}
        context = self.context

        # Create the various other pages
        self.add_page(self.home_page, k_home_page)
        printpage = self.add_page(PrintPage(context), k_print_page)
        self.add_page(ControlPage(context), k_control_page)
        self.add_page(TemperaturePage(context), k_temperature_page)
        self.add_page(SettingsPage(context), k_settings_page)
        self.add_page(DebugPage(context), k_debug_page)
        self.add_page(InfoPage(context), k_info_page)
        self.add_page(SerialPage(context), k_serial_page)
        self.add_page(UserUpdatePage(context), k_userupdate_page)
        self.add_page(DuExSetupPage(context), k_duexsetup_page)

        # Start the UI on the Home page
        self.stack.setCurrentWidget(self.home_page)

        # Create the data structure that will contain the stack of
        # pages to display.
        self.page_stack = []

        # Activate the window to take keyboard focus.
        self.setWindowState(Qt.WindowActive)
        self.activateWindow()

        context.printer_if.set_state_changed_callback(
            self.state_changed_callback)
        self.setStyleProperty(self.status, "bottom_bar")
        self.setAllStyleProperty(
            [self.right_status, self.left_status, self.middle_status], "white-transparent-text")

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
