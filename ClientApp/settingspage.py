import logging

from PyQt5.QtCore import Qt

from constants import *

from . import serialsetup
from . import server
from .info import InfoWindow
from .debugpage import DebugPage
from .dualex import DuExSetupWindow
from .basepage import BasePage

from .qt.settingspage_qt import Ui_SettingsPage

class SettingsPage(BasePage, Ui_SettingsPage):
    def __init__(self, context):

        super(SettingsPage, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("SerialWindow __init__()")

        # Set up UI
        self.setupUi(self)

        # Save reference to printer interface
        self.printer_if = context.printer_if
        self.personality = context.personality
        self.ui_controller = context.ui_controller

        # self.debug_window = DebugWindow(self.printer_if, self.personality, self)
        # self.info_window = InfoWindow(self.printer_if, self)
        # self.duex_window = DuExSetupWindow(self.printer_if, self)

        self.setbuttonstyle(self.Serial)
        self.setbuttonstyle(self.Server)
        self.setbuttonstyle(self.UserUpdate)
        self.setbuttonstyle(self.Wifi)
        self.setbuttonstyle(self.Back)

        self.setbuttonstyle(self.w_pushbutton_debug)
        self.setbuttonstyle(self.w_pushbutton_duex)
        self.setbuttonstyle(self.w_pushbutton_info)
        self.setbuttonstyle(self.w_pushbutton_term)

        # versiontext = "v"+QtWidgets.QApplication.instance().applicationVersion()
        # self.SoftwareVersion.setText(versiontext)

        # self.Serial.clicked.connect(self.serialpop)
        # self.Server.clicked.connect(self.serverpop)
        # self.UserUpdate.clicked.connect(self.userupdatepop)
        self.w_pushbutton_debug.clicked.connect(self.handle_debug)
        # self.w_pushbutton_info.clicked.connect(self.handle_info)
        # self.w_pushbutton_duex.clicked.connect(self.handle_duex)
        # self.w_pushbutton_term.clicked.connect(self.handle_term)

        # self.Wifi.clicked.connect(self.wifipop)
        # self.Back.clicked.connect(self.back)
        self.Back.clicked.connect(self.back)

    def _log(self, message):
        self._logger.debug(message)

    def userupdatepop(self):
        self._log("UI: User touched Update")
        self.userupdate_pop.show()
        self.close()
        self.Back.clicked.connect(self.user_back)

    def serialpop(self):
        self._log("UI: User touched Serial")
        if self.fullscreen:
            self.serial_pop.showFullScreen()
        else:
            self.serial_pop.show()

    def serverpop(self):
        self._log("UI: User touched Server")
        if self.fullscreen:
            self.server_pop.showFullScreen()
        else:
            self.server_pop.show()

    def handle_debug(self):
        self._log("UI: User touched Debug")
        self.ui_controller.push(k_debug_page)
        # if self.fullscreen:
        #     self.debug_window.showFullScreen()
        # else:
        #     self.debug_window.show()

    def handle_info(self):
        self._log("UI: User touched Info")
        if self.fullscreen:
            self.info_window.showFullScreen()
        else:
            self.info_window.show()

    def handle_duex(self):
        self._log("UI: User touched Dual Extruder")
        self.duex_window.get_settings()
        if self.fullscreen:
            self.duex_window.showFullScreen()
        else:
            self.duex_window.show()

    def handle_term(self):
        self._log("UI: User touched Term")
        # is_not_defined()

    def user_back(self):
        self._log("UI: User touched Back")
        self.close()
