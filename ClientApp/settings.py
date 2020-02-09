from PyQt5.QtCore import Qt
from .qt.settingswindow import *
from . import serialsetup
from . import server
from .basewindow import BaseWindow


class SettingsWindow(BaseWindow, Ui_SettingsWindow):
    def __init__(self, client_obj, serial_obj, parent=None):
        super(SettingsWindow, self).__init__(parent)
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

    def serialpop(self):
        self.serial_pop.show()
        self.close()

    def serverpop(self):
        self.server_pop.show()
        self.close()

    def userupdatepop(self):
        self.userupdate_pop.show()
        self.close()