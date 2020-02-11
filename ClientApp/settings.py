import logging
from PyQt5.QtCore import Qt
from .qt.settingswindow import *
from . import serialsetup
from . import server

class SettingsWindow(QtWidgets.QWidget, Ui_SettingsWindow):
    def __init__(self, client_obj, serial_obj, parent=None):
        super(SettingsWindow, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("SerialWindow __init__()")

        # Set up UI
        self.setupUi(self)
        self.client_obj = client_obj
        self.serial_obj = serial_obj
        self.parent = parent
        self.parent.setbuttonstyle(self.Serial)
        self.parent.setbuttonstyle(self.Server)

        if parent.fullscreen:
            self.fullscreen = True
        else:
            self.fullscreen = False

        self.Serial.clicked.connect(self.serialpop)
        self.Server.clicked.connect(self.serverpop)
        self.Back.clicked.connect(self.user_back)

    def _log(self, message):
        self._logger.debug(message)

    def user_back(self):
        self._log("UI: User touch Back")
        self.close()

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
