from qt.touchdisplaywindow import *
from PyQt5.QtCore import Qt
from control import *
from temperature import *
from settings import *
import sys

class TouchDisplay(QtWidgets.QWidget, Ui_TouchDisplay):
    def __init__(self, client, serial, parent = None):
        super(TouchDisplay, self).__init__()
        self.setupUi(self)

        self.fullscreen = True
        if self.fullscreen: 
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        self.client = client
        self.serial = serial

        self.Control.setCheckable(False)
        #self.Control.setStyleSheet("QPushButton{background: rgba(255,255,255,0); outline: none; border: none;} QPushButton:checked{background: rgba(255,255,255,0); outline: none; border: none;} QPushButton:pressed {background: rgba(255,255,255,0); outline: none; border: none;}")
        self.setbuttonstyle(self.Print)
        self.setbuttonstyle(self.Settings)
        self.setbuttonstyle(self.Control)
        self.setbuttonstyle(self.Temperature)
        #self.Print.setStyleSheet("QPushButton{background: rgba(255,255,255,0); outline: none; border: none;} QPushButton:checked{background: rgba(255,255,255,0); outline: none; border: none;} QPushButton:pressed {background: rgba(255,255,255,0); outline: none; border: none;}")
        #self.Settings.setStyleSheet("QPushButton{background: rgba(255,255,255,0); outline: none; border: none;} QPushButton:checked{background: rgba(255,255,255,0); outline: none; border: none;} QPushButton:pressed {background: rgba(255,255,255,0); outline: none; border: none;}")
        
        self.set_pop = SettingsWindow(self.client, self.serial, self)
        self.temp_pop = TemperatureWindow(self.serial, self)
        self.con_pop = ControlWindow(self.serial, self)

        self.Control.clicked.connect(self.controlpop)
        self.Temperature.clicked.connect(self.temperaturepop)
        self.Settings.clicked.connect(self.settingspop)
    def controlpop(self):
        if self.fullscreen: self.con_pop.showFullScreen()
        else: self.con_pop.show()
    def temperaturepop(self):
        if self.fullscreen: self.temp_pop.showFullScreen()
        else: self.temp_pop.show()
    def settingspop(self): 
        if self.fullscreen: self.set_pop.showFullScreen()
        else: self.set_pop.show()
    def setbuttonstyle(self,obj):
        obj.setStyleSheet("QPushButton{background: rgba(255,255,255,0); outline: none; border: none;} QPushButton:checked{background: rgba(255,255,255,0); outline: none; border: none;} QPushButton:pressed {background: rgba(0,0,0,0.08); outline: none; border: none;}")

