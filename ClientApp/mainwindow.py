import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QWidget, QLabel

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

        # # Initialize the widgets in the status bar.
        # status_parent = QWidget()
        # status_content = Ui_Status()
        # status_content.setupUi(status_parent)
        # self.status_content = status_content
        # self.statusbar.addPermanentWidget(status_parent)

        # stat_parent2 = QWidget()
        # self.stat2 = Ui_Status()
        # self.stat2.setupUi(stat_parent2)
        # self.statusbar.addWidget(stat_parent2)

        # # foo = QLabel()
        # # foo.setText("foo")
        # # self.statusbar.addWidget(foo)

        # # bar = QLabel()
        # # bar.setText("bar")
        # # self.statusbar.addWidget(bar)

        # # self.status_content.left.setText("Hello, world, again.")

        # self.centralwidget.setFixedHeight(448)
        # self.statusbar.setFixedWidth(800)
        # self.statusbar.setFixedHeight(32)

        self.home_page = HomePage(self.context)
        self.stack.addWidget(self.home_page)

        self.pages = {}
        context = self.context

        # Create the various pages
        self.add_page(PrintPage(context), k_print_page)
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
                self._log("<%s> just_pushed callback exists, calling..." % page_name)
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
