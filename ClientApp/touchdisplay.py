from qt.touchdisplaywindow import *
from PyQt5.QtCore import Qt
from control import *
from temperature import *
from settings import *
from printwindow import *
import sys


class TouchDisplay(QtWidgets.QWidget, Ui_TouchDisplay):
    def __init__(self, client, serial, fullscreen=True, parent=None):
        super(TouchDisplay, self).__init__()
        self.setupUi(self)

#       Change fullscreen to True if uploading to Raspberrypi
        self.fullscreen = fullscreen
        if self.fullscreen:
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        self.client = client
        self.serial = serial

        self.setbuttonstyle(self.Print)
        self.setbuttonstyle(self.Settings)
        self.setbuttonstyle(self.Control)
        self.setbuttonstyle(self.Temperature)

#       Event handler object that handles temperature materials, flowrate, etc.
        self.event_handler = event_handler(self.serial)

        self.set_pop = SettingsWindow(self.client, self.serial, self)
        self.server_pop = ServerWindow(self.client, self.set_pop)
        self.serial_pop = SerialWindow(
            self.serial, self.event_handler, self.set_pop)
        self.set_pop.serial_pop = self.serial_pop
        self.set_pop.server_pop = self.server_pop

        self.temp_pop = TemperatureWindow(
            self.serial, self.event_handler, self)
        self.con_pop = ControlWindow(self.serial, self)
        self.print_pop = PrintWindow(self.serial, self.temp_pop, self)

        self.event_handler.tempwindow = self.temp_pop
        self.event_handler.serialwindow = self.serial_pop
        self.event_handler.start()

        self.Control.clicked.connect(self.controlpop)
        self.Temperature.clicked.connect(self.temperaturepop)
        self.Settings.clicked.connect(self.settingspop)
        self.Print.clicked.connect(self.printpop)

    def controlpop(self):
        if self.fullscreen:
            self.con_pop.showFullScreen()
        else:
            self.con_pop.show()

    def temperaturepop(self):
        if self.fullscreen:
            self.temp_pop.showFullScreen()
        else:
            self.temp_pop.show()

    def settingspop(self):
        if self.fullscreen:
            self.set_pop.showFullScreen()
        else:
            self.set_pop.show()

    def printpop(self):
        if self.fullscreen:
            self.print_pop.showFullScreen()
        else:
            self.print_pop.show()

    def setbuttonstyle(self, obj):
        obj.setStyleSheet(
            "QPushButton{background: rgba(255,255,255,0); outline: none; border: none;} QPushButton:checked{background: rgba(255,255,255,0); outline: none; border: none;} QPushButton:pressed {background: rgba(0,0,0,0.08); outline: none; border: none;}")
