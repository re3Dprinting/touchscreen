import logging

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from constants import Pages

#from  import serialsetup
#from  import server
# from dualex import DuExSetupWindow

from basepage import BasePage

from qt.settingspage_qt import Ui_SettingsPage


class SettingsPage(BasePage, Ui_SettingsPage):
    def __init__(self, context):

        super(SettingsPage, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log_d("SettingsPage __init__()")

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
        QtWidgets.QScroller.grabGesture(
            self.SettingsScrollArea, QtWidgets.QScroller.LeftMouseButtonGesture)

        self.setStyleProperty(self.BottomBar, "bottom-bar")
        self.setAllTransparentButton([self.Back], True)
        self.setAllTransparentButton([self.Serial, self.Server, self.UserUpdate, self.Wifi,
                                      self.w_pushbutton_debug, self.w_pushbutton_duex, self.w_pushbutton_info, self.w_pushbutton_term])

        self.Back.clicked.connect(self.back)

    def userupdatepop(self):
        self._log_d("UI: User touched Update")
        self.ui_controller.push(Pages.USERUPDATE_PAGE)

    def serialpop(self):
        self._log_d("UI: User touched Serial")
        self.ui_controller.push(Pages.SERIAL_PAGE)

    def serverpop(self):
        self._log_d("UI: User touched Server")

    def handle_debug(self):
        self._log_d("UI: User touched Debug")
        self.ui_controller.push(Pages.DEBUG_PAGE)

    def handle_info(self):
        self._log_d("UI: User touched Info")
        self.ui_controller.push(Pages.INFO_PAGE)

    def handle_duex(self):
        self._log_d("UI: User touched Dual Extruder")
        self.ui_controller.push(Pages.DUEXSETUP_PAGE)

    def handle_term(self):
        self._log_d("UI: User touched Term")
        # is_not_defined()

    def user_back(self):
        self._log_d("UI: User touched Back")
        self.close()
