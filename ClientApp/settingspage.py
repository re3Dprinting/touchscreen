import logging

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from constants import *

#from . import serialsetup
#from . import server
# from .dualex import DuExSetupWindow

from .basepage import BasePage

from .qt.settingspage_qt import Ui_SettingsPage


class SettingsPage(BasePage, Ui_SettingsPage):
    def __init__(self, context):

        super(SettingsPage, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("SettingsPage __init__()")

        # Set up UI
        self.setupUi(self)

        # Save reference to printer interface
        self.printer_if = context.printer_if
        self.personality = context.personality
        self.ui_controller = context.ui_controller

        self.setAllTransparentButton([self.Serial, self.Server, self.UserUpdate, self.Wifi,
                                      self.w_pushbutton_debug, self.w_pushbutton_duex, self.w_pushbutton_info, self.w_pushbutton_term])

        self.Serial.clicked.connect(self.serialpop)
        self.Server.clicked.connect(self.serverpop)
        self.UserUpdate.clicked.connect(self.userupdatepop)
        self.w_pushbutton_debug.clicked.connect(self.handle_debug)
        self.w_pushbutton_info.clicked.connect(self.handle_info)
        self.w_pushbutton_duex.clicked.connect(self.handle_duex)

        self.SettingsScrollArea.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        # self.SettingsScrollArea.setHorizontalScrollBarPolicy(
        #     Qt.ScrollBarAlwaysOff)
        QtWidgets.QScroller.grabGesture(
            self.SettingsScrollArea, QtWidgets.QScroller.LeftMouseButtonGesture)

        self.setStyleProperty(self.BottomBar, "bottom-bar")
        self.setAllTransparentButton([self.Back], True)
        self.setAllTransparentButton([self.Serial, self.Server, self.UserUpdate, self.Wifi,
                                      self.w_pushbutton_debug, self.w_pushbutton_duex, self.w_pushbutton_info, self.w_pushbutton_term])

        # self.w_pushbutton_term.clicked.connect(self.handle_term)
        # self.Wifi.clicked.connect(self.wifipop)
        # self.Back.clicked.connect(self.back)
        self.Back.clicked.connect(self.back)

    def _log(self, message):
        self._logger.debug(message)

    def userupdatepop(self):
        self._log("UI: User touched Update")
        self.ui_controller.push(k_userupdate_page)

    def serialpop(self):
        self._log("UI: User touched Serial")
        self.ui_controller.push(k_serial_page)

    def serverpop(self):
        self._log("UI: User touched Server")

    def handle_debug(self):
        self._log("UI: User touched Debug")
        self.ui_controller.push(k_debug_page)

    def handle_info(self):
        self._log("UI: User touched Info")
        self.ui_controller.push(k_info_page)

    def handle_duex(self):
        self._log("UI: User touched Dual Extruder")
        # NOTE: when pushing this page, the just_pushed callback will
        # allow the DuEx widget to load the current settings.
        self.ui_controller.push(k_duexsetup_page)

    def handle_term(self):
        self._log("UI: User touched Term")
        # is_not_defined()

    def user_back(self):
        self._log("UI: User touched Back")
        self.close()
