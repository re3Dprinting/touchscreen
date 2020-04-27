import sys
import logging

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
#import PyQt5

# #from . import control
# #from . import temperature
# from .control import ControlWindow
# #from . import printwindow
# from .printwindow import PrintWindow
# from . import settings
# from .event_hand import event_handler
# from .settings import SettingsWindow
# from .server import ServerWindow
# from .serialsetup import SerialWindow
# from .temperature import TemperatureWindow
# from .userupdate import UserUpdateWindow
# from .basewindow import BaseWindow
# from .notification import Notification
# #from . import event_hand

from .qt.home_qt import Ui_Home
from constants import *
from basepage import BasePage

class HomePage(BasePage, Ui_Home):
    def __init__(self, context):
        super(HomePage, self).__init__()

        self.printer_if = context.printer_if
        self.personality = context.personality
        self.ui_controller = context.ui_controller
        
        # Initialize the UI
        self.setupUi(self)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("HomePage starting up")

        # Save the personality spec
        
        versiontext = "v"+ QtWidgets.QApplication.instance().applicationVersion()
        self.SoftwareVersion.setText(versiontext)

        self.setbuttonstyle(self.pushbutton_print)
        self.setbuttonstyle(self.pushbutton_control)
        self.setbuttonstyle(self.pushbutton_temperature)
        self.setbuttonstyle(self.pushbutton_settings)
        self.setbuttonstyle(self.pushbutton_back)

        self.pushbutton_print.clicked.connect(self.handle_print_touch)
        self.pushbutton_control.clicked.connect(self.handle_control_touch)
        self.pushbutton_temperature.clicked.connect(self.handle_temperature_touch)
        self.pushbutton_settings.clicked.connect(self.handle_settings_touch)
        self.pushbutton_back.clicked.connect(self.handle_back_touch)

#       Event handler object that handles temperature materials, flowrate, etc.
#        self.event_handler = event_handler(self.printer_if)

        # self.set_pop = SettingsWindow(personality, self.printer_if, self)
        # self.server_pop = ServerWindow(self.set_pop)


        # self.userupdate_pop = UserUpdateWindow(self.personality, self.set_pop)
        # self.notification = self.userupdate_pop.checkupdate()

        # self.serial_pop = SerialWindow(
        #     self.printer_if, self.event_handler, self.set_pop)

        # self.set_pop.serial_pop = self.serial_pop
        # self.set_pop.server_pop = self.server_pop
        # self.set_pop.userupdate_pop = self.userupdate_pop

        # self.temp_pop = TemperatureWindow(self.printer_if, self.event_handler, self)
        # self.con_pop = ControlWindow(self.printer_if, self)
        # self.print_pop = PrintWindow(self.printer_if, self.temp_pop, self.personality, self)

        # self.event_handler.tempwindow = self.temp_pop
        # self.event_handler.serialwindow = self.serial_pop
        # self.event_handler.start()

    def handle_print_touch(self):
        self._log("UI: User touched Print")
        self.ui_controller.push(k_print_page)

    def handle_control_touch(self):
        self._log("UI: User touched Control")
        self.ui_controller.push(k_control_page)

    def handle_temperature_touch(self):
        self._log("UI: User touched Temperature")
        self.ui_controller.push(k_temperature_page)

    def handle_settings_touch(self):
        self._log("UI: User touched Settings")
        self.ui_controller.push(k_settings_page)        

    def handle_back_touch(self):
        self._log("UI: User touched Back")
        self.ui_controller.pop()
        
