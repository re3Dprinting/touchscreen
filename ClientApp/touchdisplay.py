import sys
import logging

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
from .temperature import TemperatureWindow
from .basewindow import BaseWindow
#from . import event_hand

from .qt.touchdisplaywindow import Ui_TouchDisplay


class TouchDisplay(BaseWindow, Ui_TouchDisplay):
    def __init__(self, printer_if, personality, parent=None):
        super(TouchDisplay, self).__init__(parent)
        self.personality = personality
        
        # Initialize the UI
        self.setupUi(self)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("PrinterIF starting up")

        # Save the personality spec
        self.personality = personality
        
#       Change fullscreen to True if uploading to Raspberrypi
        self.fullscreen = personality.fullscreen
        if self.fullscreen:
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        versiontext = "v"+ QtWidgets.QApplication.instance().applicationVersion()
        self.SoftwareVersion.setText(versiontext)

        self.printer_if = printer_if

        #Set Button style of buttons. see Basewindow function, setbuttonstyle.
        self.setbuttonstyle(self.Print)
        self.setbuttonstyle(self.Settings)
        self.setbuttonstyle(self.Control)
        self.setbuttonstyle(self.Temperature)

        # Event handler object that handles temperature materials, flowrate, etc.
        self.event_handler = event_handler(self.printer_if)

        self.set_pop = SettingsWindow(personality, self.printer_if, self.event_handler, self)
        self.temp_pop = TemperatureWindow(self.printer_if, self.event_handler, self)
        self.con_pop = ControlWindow(self.printer_if, self)
        self.print_pop = PrintWindow(self.printer_if, self.temp_pop, self.personality, self)

        self.event_handler.tempwindow = self.temp_pop
        self.event_handler.serialwindow = self.set_pop.serial_pop
        self.event_handler.start()

        self.Control.clicked.connect(self.controlpop)
        self.Temperature.clicked.connect(self.temperaturepop)
        self.Settings.clicked.connect(self.settingspop)
        self.Print.clicked.connect(self.printpop)

    def controlpop(self):
        self._log("UI: User touched Control")
        self.con_pop.show()
        self.close()

    def temperaturepop(self):
        self._log("UI: User touched Temperature")
        self.temp_pop.show()
        self.close()

    def settingspop(self):
        self._log("UI: User touched Settings")
        self.set_pop.show()
        self.close()

    def printpop(self):
        self._log("UI: User touched Print")
        self.print_pop.show()
        self.close()
