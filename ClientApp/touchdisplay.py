import sys

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
#import PyQt5

#from . import control
#from . import temperature
from .control import ControlWindow
#from . import printwindow
from .printwindow import PrintWindow
from . import settings
from .event_hand import event_handler
from .settings import SettingsWindow
from .server import ServerWindow
from .serialsetup import SerialWindow
from .temperature import TemperatureWindow
#from . import event_hand

from .qt.touchdisplaywindow import Ui_TouchDisplay

class TouchDisplay(QtWidgets.QWidget, Ui_TouchDisplay):
    def __init__(self, client, printer_if, personality, parent=None):
        super(TouchDisplay, self).__init__()
        self.personality = personality
        
        self.setupUi(self)

#       Change fullscreen to True if uploading to Raspberrypi
        self.fullscreen = personality.fullscreen
        if self.fullscreen:
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        self.client = client
        self.printer_if = printer_if

        self.setbuttonstyle(self.Print)
        self.setbuttonstyle(self.Settings)
        self.setbuttonstyle(self.Control)
        self.setbuttonstyle(self.Temperature)

#       Event handler object that handles temperature materials, flowrate, etc.
        self.event_handler = event_handler(self.printer_if)

        self.set_pop = SettingsWindow(self.client, self.printer_if, self)
        self.server_pop = ServerWindow(self.client, self.set_pop)
        self.serial_pop = SerialWindow(
            self.printer_if, self.event_handler, self.set_pop)
        self.set_pop.serial_pop = self.serial_pop
        self.set_pop.server_pop = self.server_pop

        self.temp_pop = TemperatureWindow(
            self.printer_if, self.event_handler, self)
        self.con_pop = ControlWindow(self.printer_if, self)
        self.print_pop = PrintWindow(self.printer_if, self.temp_pop, self.personality, self)

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
