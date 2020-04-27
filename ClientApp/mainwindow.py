import logging

from PyQt5 import QtWidgets

from .qt.mainwindow_qt import Ui_MainWindow

from constants import *
from context import Context

from .homepage import HomePage
from .printpage import PrintPage
from .controlpage import ControlPage

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
        self.stack.setCurrentWidget(self.home_page)

        self.pages = {}

        # Create the Print page
        context = self.context
        self.add_page(PrintPage(context), k_print_page)
        self.add_page(ControlPage(context), k_control_page)
        
        # self.print_page = PrintPage(self.context)
        # self.add_page(self.print_page, k_print_page)
        # self.stack.addWidget(self.print_page)
        # self.pages[k_print_page] = self.print_page

        # Create the Control page
        # self.control_page = ControlPage(self.context)
        # self.stack.addWidget(self.control_page)
        # self.pages[k_control_page] = self.control_page

    def add_page(self, page, page_name):
        self.stack.addWidget(page)
        self.pages[page_name] = page
        return page

    def _log(self, message):
        self._logger.debug(message)

    def push(self, page_name):
        try:
            widget = self.pages[page_name]
            self.stack.setCurrentWidget(widget)
        except KeyError:
            self._log("MainWindow: page \"%s\" not found." % page_name)
        
    def pop(self):
        self.stack.setCurrentWidget(self.home_page)
