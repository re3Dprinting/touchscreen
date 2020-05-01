import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .qt.mainwindow_qt import Ui_MainWindow

from constants import *
from context import Context

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

class MainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, printer_if, persona):
        super(MainWindow, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("PrinterIF starting up")

        self.context = Context(printer_if, persona, self)

        # Initialize the UI
        self.setupUi(self)
        self.centralwidget.setFixedHeight(448)
        self.statusbar.setFixedHeight(32)

        self.statusBar().showMessage("Hello, world")

        self.home_page = HomePage(self.context)
        self.stack.addWidget(self.home_page)

        self.pages = {}
        context = self.context

        # Create the various pages
        self.print_page = self.add_page(PrintPage(context), k_print_page)
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

        self.page_stack = []

        # Activate the window to take keyboard focus.
        self.setWindowState(Qt.WindowActive)
        self.activateWindow()

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

    def push(self, page_name):
        try:
            # Get the widget we're going to display next.
            widget = self.pages[page_name]

            # Get the current widget being display and push it onto
            # the page stack so we can pop back to it later.
            self.page_stack.append(self.stack.currentWidget())

            # Display the next widget
            self.stack.setCurrentWidget(widget)

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
