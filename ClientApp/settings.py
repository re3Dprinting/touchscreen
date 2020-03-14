import logging
from PyQt5.QtCore import Qt
from .qt.settingswindow import *
from . import serialsetup
from . import server
from .info import InfoWindow
from .debug import DebugWindow
from .basewindow import BaseWindow


class SettingsWindow(BaseWindow, Ui_SettingsWindow):
    def __init__(self, personality, printer_if, parent=None):

        super(SettingsWindow, self).__init__(parent)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("SerialWindow __init__()")

        # Set up UI
        self.setupUi(self)

        # Save reference to printer interface
        self.printer_if = printer_if

        self.debug_window = DebugWindow(printer_if, personality, self)
        self.info_window = InfoWindow(printer_if, self)
        

        self.parent.setbuttonstyle(self.Serial)
        self.parent.setbuttonstyle(self.Server)
        self.parent.setbuttonstyle(self.UserUpdate)
        self.parent.setbuttonstyle(self.Wifi)
        self.parent.setbuttonstyle(self.w_pushbutton_debug)
        self.parent.setbuttonstyle(self.w_pushbutton_stats)
        self.parent.setbuttonstyle(self.w_pushbutton_info)
        self.parent.setbuttonstyle(self.w_pushbutton_term)

        versiontext = "v"+QtWidgets.QApplication.instance().applicationVersion()
        self.SoftwareVersion.setText(versiontext)

        self.Serial.clicked.connect(self.serialpop)
        self.Server.clicked.connect(self.serverpop)
        self.UserUpdate.clicked.connect(self.userupdatepop)

        self.w_pushbutton_debug.clicked.connect(self.handle_debug)
        self.w_pushbutton_info.clicked.connect(self.handle_info)
        self.w_pushbutton_stats.clicked.connect(self.handle_stats)
        self.w_pushbutton_term.clicked.connect(self.handle_term)

        # self.Wifi.clicked.connect(self.wifipop)
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
        if self.fullscreen:
            self.debug_window.showFullScreen()
        else:
            self.debug_window.show()

    def handle_info(self):
        self._log("UI: User touched Info")
        if self.fullscreen:
            self.info_window.showFullScreen()
        else:
            self.info_window.show()

    def handle_stats(self):
        self._log("UI: User touched Stats")

    def handle_term(self):
        self._log("UI: User touched Term")
        # is_not_defined()

    def user_back(self):
        self._log("UI: User touched Back")
        self.close()
