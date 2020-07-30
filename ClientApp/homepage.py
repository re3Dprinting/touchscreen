import sys
import logging

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

from .qt.home_qt import Ui_Home
from constants import Pages
from basepage import BasePage


class HomePage(BasePage, Ui_Home):
    def __init__(self, context):
        super(HomePage, self).__init__()

        self.printer_if = context.printer_if
        self.personality = context.personality
        self.ui_controller = context.ui_controller

        # Initialize the UI
        self.setupUi(self)

        self._logger = logging.getLogger(__name__)
        self._log_d("HomePage __init__()")

        # Save the personality spec

        self.setTransparentIcon(self.re3DIcon)
        self.setAllTransparentButton(
            [self.pushbutton_print, self.pushbutton_control, self.pushbutton_temperature, self.pushbutton_settings])
#        self.setTransparentButton(self.pushbutton_back)

        self.pushbutton_print.clicked.connect(self.handle_print_touch)
        self.pushbutton_control.clicked.connect(self.handle_control_touch)
        self.pushbutton_temperature.clicked.connect(self.handle_temperature_touch)
        self.pushbutton_settings.clicked.connect(self.handle_settings_touch)

    def handle_print_touch(self):
        self._log_d("UI: User touched Print")
        self.ui_controller.push(Pages.PRINT_PAGE)

    def handle_control_touch(self):
        self._log_d("UI: User touched Control")
        self.ui_controller.push(Pages.CONTROL_PAGE)

    def handle_temperature_touch(self):
        self._log_d("UI: User touched Temperature")
        self.ui_controller.push(Pages.TEMPERATURE_PAGE)

    def handle_settings_touch(self):
        self._log_d("UI: User touched Settings")
        self.ui_controller.push(Pages.SETTINGS_PAGE)

