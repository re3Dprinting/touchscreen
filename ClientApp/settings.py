import logging
from PyQt5.QtCore import Qt
from .qt.settingswindow import *
from . import serialsetup
from . import server
from .basewindow import BaseWindow


class SettingsWindow(BaseWindow, Ui_SettingsWindow):
    def __init__(self, client_obj, serial_obj, parent=None):
        super(SettingsWindow, self).__init__(parent)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("SerialWindow __init__()")

        # Set up UI
        self.setupUi(self)
        self.client_obj = client_obj
        self.serial_obj = serial_obj
        self.parent.setbuttonstyle(self.Serial)
        self.parent.setbuttonstyle(self.Server)
        self.parent.setbuttonstyle(self.UserUpdate)
        self.parent.setbuttonstyle(self.Wifi)

        versiontext = "v"+QtWidgets.QApplication.instance().applicationVersion()
        self.SoftwareVersion.setText(versiontext)

        self.Serial.clicked.connect(self.serialpop)
        self.Server.clicked.connect(self.serverpop)
        self.UserUpdate.clicked.connect(self.userupdatepop)

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

    def user_back(self):
        self._log("UI: User touched Back")
        self.close()
