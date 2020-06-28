from builtins import str
import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .qt.controlpage_qt import Ui_ControlPage
from .axis import Axis
from .basepage import BasePage

increments_str = ["01", "1", "10", "100"]
increments_int = ['0.1', '1', '10', '100']


class ControlPage(BasePage, Ui_ControlPage):
    def __init__(self, context):
        super(ControlPage, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("ControlPage __init__()")

        # Set up UI
        self.setupUi(self)

        # Save reference to context objects
        self.printer_if = context.printer_if
        self.ui_controller = context.ui_controller

        # self.timer.timeout.connect(lambda: self.button_event_check())
        self.xinc = None
        self.yinc = None
        self.zinc = None
        self.einc = None
        self.currentextruder = None

        self.setTransparentButton(self.Back)
        self.setTransparentButton(self.DisableMotors)
        self.setTransparentButton(self.HomeAll)
        self.setTransparentButton(self.HomeXY)
        self.setTransparentButton(self.HomeZ)
        self.setTransparentIcon(self.movex)
        self.setTransparentIcon(self.movey)
        self.setTransparentIcon(self.movez)
        self.setTransparentIcon(self.movee)
        self.xbutton = self.AddButtontoGroup("x")
        self.ybutton = self.AddButtontoGroup("y")
        self.zbutton = self.AddButtontoGroup("z")
        self.ebutton = self.AddButtontoGroup("e")

        self.xaxis = Axis("x", "4500", self, 25)
        self.yaxis = Axis("y", "4500", self, 25)
        self.zaxis = Axis("z", "4500", self, 2)
        self.eaxis = Axis("e0", "60", self)
        self.e1axis = Axis("e1", "60", self)

        self.inittextformat(self.PositionLabel)
        # self.serial.data.updateposition.connect(self.updateposition)

        self.HomeXY.clicked.connect(self.homexy)
        self.HomeZ.clicked.connect(self.homez)
        self.HomeAll.clicked.connect(self.homeall)

        self.Back.clicked.connect(self.back)

        self.DisableMotors.clicked.connect(self.disablemotors)
        self.Back.clicked.connect(self.user_back)

    def user_back(self):
        self._log("UI: User touched Back")
        self.close()

    def updateposition(self):
        # pos = self.serial.data.position
        pos = 0
        tmp = "X: "+str(pos["X"]) + " Y: "+str(pos["Y"]) + " Z: "+str(pos["Z"])
        self.changeText(self.PositionLabel, tmp)

    def disablemotors(self):
        # self.serial.send_serial('M18')
        self._log("UI: User touched Motor enable/disable")
        self.printer_if.commands("M18", force=True)
        pass

    def homexy(self):
        # self.serial.send_serial('G28 XY')
        self._log("UI: User touched Home XY")
        self.printer_if.homexy()

    def homez(self):
        # self.serial.send_serial('G28 Z')
        self._log("UI: User touched Home Z")
        self.printer_if.homez()

    def homeall(self):
        # self.serial.send_serial('G28')
        self._log("UI: User touched Home All")
        self.printer_if.homeall()

    def AddButtontoGroup(self, axis):
        group = QtWidgets.QButtonGroup(self)
        for i in increments_str:
            att = axis + "m" + i
            self.SetButtonSettings(getattr(self, att))
            group.addButton(getattr(self, att))
        getattr(self, axis + "m"+"10").setChecked(True)
        return group

    def SetButtonSettings(self, obj):
        obj.setCheckable(True)
        obj.setProperty("cssClass", "axis_button")

    def changeText(self, label, text):
        tmp = QtWidgets.QApplication.translate(
            "TemperatureWindow", label.format[0]+text+label.format[1], None, -1)
        label.setText(tmp)

    def inittextformat(self, label):
        label.format = label.text()
        label.format = label.format.split("-----")
