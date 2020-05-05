import logging
from PyQt5.QtCore import Qt
from .qt.settingswindow import *
from . import serialsetup
from . import server
from .info import InfoWindow
from .debug import DebugWindow
from .dualex import DuExSetupWindow
from .userupdate import UserUpdateWindow
from .serialsetup import SerialWindow
from .notification import Notification
from .server import ServerWindow
from .basewindow import BaseWindow


class SettingsWindow(BaseWindow, Ui_SettingsWindow):
    def __init__(self, personality, printer_if, event_handler, parent=None):

        super(SettingsWindow, self).__init__(parent)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("SerialWindow __init__()")

        # Set up UI
        self.setupUi(self)

        # Save reference to printer interface
        self.printer_if = printer_if
        self.event_handler = event_handler

        #Create instances of each sub-window of the settings menu. 
        self.debug_window = DebugWindow(printer_if, personality, self)
        self.info_window = InfoWindow(printer_if, self)
        self.duex_window = DuExSetupWindow(printer_if, self)
        self.userupdate_pop = UserUpdateWindow(personality, self)
        self.notification = self.userupdate_pop.checkupdate()
        self.serial_pop = SerialWindow(
            self.printer_if, self.event_handler, self)
        self.server_pop = ServerWindow(self)
        
        
        #Setup the button style from the baseclass function, setbuttonstyle
        self.setbuttonstyle(self.Serial)
        self.setbuttonstyle(self.Server)
        self.setbuttonstyle(self.UserUpdate)
        self.setbuttonstyle(self.Wifi)
        self.setbuttonstyle(self.w_pushbutton_debug)
        self.setbuttonstyle(self.w_pushbutton_duex)
        self.setbuttonstyle(self.w_pushbutton_info)
        self.setbuttonstyle(self.w_pushbutton_term)

        versiontext = "v"+QtWidgets.QApplication.instance().applicationVersion()
        self.SoftwareVersion.setText(versiontext)


        self.Serial.clicked.connect(self.serialpop)
        self.Server.clicked.connect(self.serverpop)
        self.UserUpdate.clicked.connect(self.userupdatepop)
        self.w_pushbutton_debug.clicked.connect(self.handle_debug)
        self.w_pushbutton_info.clicked.connect(self.handle_info)
        self.w_pushbutton_duex.clicked.connect(self.handle_duex)
        self.w_pushbutton_term.clicked.connect(self.handle_term)

        # self.Wifi.clicked.connect(self.wifipop)
        self.Back.clicked.connect(self.back)

    def userupdatepop(self):
        self._log("UI: User touched Update")
        self.userupdate_pop.show()
        self.close()

    def serialpop(self):
        self._log("UI: User touched Serial")
        self.serial_pop.show()
        self.close()

    def serverpop(self):
        self._log("UI: User touched Server")
        self.server_pop.show()
        self.close()

    def handle_debug(self):
        self._log("UI: User touched Debug")
        self.debug_window.show()
        self.close()

    def handle_info(self):
        self._log("UI: User touched Info")
        self.info_window.show()
        self.close()

    def handle_duex(self):
        self._log("UI: User touched Dual Extruder")
        self.duex_window.get_settings()
        self.duex_window.show()
        self.close()

    def handle_term(self):
        self._log("UI: User touched Term")
        # is_not_defined()

