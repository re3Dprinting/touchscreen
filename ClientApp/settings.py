from qt.settingswindow import *
from PyQt5.QtCore import Qt
from serialsetup import *
from server import *


class SettingsWindow(QtWidgets.QWidget, Ui_SettingsWindow):
    def __init__(self, client_obj, serial_obj, parent=None):
        super(SettingsWindow, self).__init__()
        self.setupUi(self)
        self.client_obj = client_obj
        self.serial_obj = serial_obj
        self.parent = parent
        self.parent.setbuttonstyle(self.Serial)
        self.parent.setbuttonstyle(self.Server)
        self.parent.setbuttonstyle(self.UserUpdate)
        self.parent.setbuttonstyle(self.Wifi)

        versiontext = "v"+QtWidgets.QApplication.instance().applicationVersion()
        self.SoftwareVersion.setText(versiontext)

        if parent.fullscreen:
            self.fullscreen = True
        else:
            self.fullscreen = False

        self.Serial.clicked.connect(self.serialpop)
        self.Server.clicked.connect(self.serverpop)
        self.UserUpdate.clicked.connect(self.userupdatepop)
        # self.Wifi.clicked.connect(self.wifipop)
        self.Back.clicked.connect(self.back)

    def serialpop(self):
        if self.fullscreen:
            self.serial_pop.showFullScreen()
        else:
            self.serial_pop.show()
        self.close()

    def serverpop(self):
        if self.fullscreen:
            self.server_pop.showFullScreen()
        else:
            self.server_pop.show()
        self.close()

    def userupdatepop(self):
        if self.fullscreen:
            self.userupdate_pop.showFullScreen()
        else:
            self.userupdate_pop.show()
        self.close()

    def back(self):
        if self.fullscreen:
            self.parent.showFullScreen()
        else:
            self.parent.show()
        self.close()