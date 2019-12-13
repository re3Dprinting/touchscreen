from builtins import str
from PyQt5.QtCore import Qt
from .qt.controlwindow import *
from .axis import *

increments_str = ["01", "1", "10", "100"]
increments_int = ['0.1', '1', '10', '100']


class ControlWindow(QtWidgets.QWidget, Ui_ControlWindow):
    def __init__(self, serial, parent=None):
        super(ControlWindow, self).__init__()
        self.setupUi(self)

        # if parent.fullscreen: self.fullscreen = True
        # else: self.fullscreen = False
        # if self.fullscreen:
        # 	self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        self.parent = parent
#        self.serial = serial

        # self.timer.timeout.connect(lambda: self.button_event_check())
        self.xinc = None
        self.yinc = None
        self.zinc = None
        self.einc = None
        self.currentextruder = None

        self.parent.setbuttonstyle(self.Back)
        self.parent.setbuttonstyle(self.DisableMotors)
        self.parent.setbuttonstyle(self.HomeAll)
        self.parent.setbuttonstyle(self.HomeXY)
        self.parent.setbuttonstyle(self.HomeZ)
        self.xbutton = self.AddButtontoGroup("x")
        self.ybutton = self.AddButtontoGroup("y")
        self.zbutton = self.AddButtontoGroup("z")
        self.ebutton = self.AddButtontoGroup("e")
        self.extruder = QtWidgets.QButtonGroup(self)

#	Setup for the Extruder button group
        self.SetButtonSettings(self.E1)
        self.SetButtonSettings(self.E2)
        self.extruder.addButton(self.E1)
        self.extruder.addButton(self.E2)
        self.E1.setChecked(False)
        self.E1.setChecked(True)
        self.currentextruder = self.extruder.checkedButton().text()
        self.extruder.buttonClicked.connect(self.updatecurrentextruder)

        self.xaxis = Axis("x", "4500", self, 25)
        self.yaxis = Axis("y", "4500", self, 25)
        self.zaxis = Axis("z", "4500", self, 2)
        self.eaxis = Axis("e", "60", self)

        self.inittextformat(self.PositionLabel)
        # self.serial.data.updateposition.connect(self.updateposition)

        self.HomeXY.clicked.connect(self.homexy)
        self.HomeZ.clicked.connect(self.homez)
        self.HomeAll.clicked.connect(self.homeall)
        self.Back.clicked.connect(self.close)
        self.DisableMotors.clicked.connect(self.disablemotors)

    def updateposition(self):
        # pos = self.serial.data.position
        pos = 0
        tmp = "X: "+str(pos["X"]) + " Y: "+str(pos["Y"]) + " Z: "+str(pos["Z"])
        self.changeText(self.PositionLabel, tmp)

    def disablemotors(self):
        # self.serial.send_serial('M18')
        pass
    
    def homexy(self):
        # self.serial.send_serial('G28 XY')
        pass
    
    def homez(self):
        # self.serial.send_serial('G28 Z')
        pass
    
    def homeall(self):
        # self.serial.send_serial('G28')
        pass
    
    def updatecurrentextruder(self):
        self.currentextruder = self.extruder.checkedButton().text()
        # if self.currentextruder == "E1":
        #     self.serial.send_serial("T0")
        # elif self.currentextruder == "E2":
        #     self.serial.send_serial("T1")

    def AddButtontoGroup(self, axis):
        group = QtWidgets.QButtonGroup(self)
        for i in increments_str:
            att = axis + "m" + i
            self.SetButtonSettings(getattr(self, att))
            group.addButton(getattr(self, att))
        # group.clearCheck()
        getattr(self, axis + "m"+"10").setChecked(False)
        getattr(self, axis + "m"+"10").setChecked(True)
        return group

    def SetButtonSettings(self, obj):
        obj.setCheckable(True)
        obj.setStyleSheet("QPushButton:checked {background: rgba(255,255,255,1); font: 14pt 'Ubuntu'; border: 2px solid #888} \
			QPushButton{background: rgba(255,255,255,0); font: 14pt 'Ubuntu'; outline: none;}")

    def changeText(self, label, text):
        tmp = QtWidgets.QApplication.translate(
            "TemperatureWindow", label.format[0]+text+label.format[1], None, -1)
        label.setText(tmp)

    def inittextformat(self, label):
        label.format = label.text()
# This line was, prior to converting for python 3:
#		label.format = label.format.encode("utf-8").split("-----")
        label.format = label.format.split("-----")
