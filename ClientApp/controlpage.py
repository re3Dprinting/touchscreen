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

        self.setbuttonstyle(self.Back)
        self.setbuttonstyle(self.DisableMotors)
        self.setbuttonstyle(self.HomeAll)
        self.setbuttonstyle(self.HomeXY)
        self.setbuttonstyle(self.HomeZ)
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

        # self.serial.data.updateposition.connect(self.updateposition)

        self.HomeXY.clicked.connect(self.homexy)
        self.HomeZ.clicked.connect(self.homez)
        self.HomeAll.clicked.connect(self.homeall)

        self.Back.clicked.connect(self.back)

        self.DisableMotors.clicked.connect(self.disablemotors)
        self.Back.clicked.connect(self.user_back)

        self.updateposition(600, 60, 0)

    def user_back(self):
        self._log("UI: User touched Back")
        self.close()

    def updateposition(self, x, y, z):

        position_format = "{0:8.2f} "

        x_pos_str = position_format.format(x)
        y_pos_str = position_format.format(y)
        z_pos_str = position_format.format(z)

        self.w_lineedit_x_position.setText(x_pos_str)
        self.w_lineedit_y_position.setText(y_pos_str)
        self.w_lineedit_z_position.setText(z_pos_str)

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
    
    def updatecurrentextruder(self):
        extruder = self.extruder.checkedButton().text()
        self._log("UI: User touched Extruder <%s>" % extruder)
        self.currentextruder = extruder

        if self.currentextruder == "E1":
            # self.serial.send_serial("T0")
            self.printer_if.commands("T0")
        elif self.currentextruder == "E2":
            # self.serial.send_serial("T1")
            self.printer_if.commands("T1")

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
        obj.setStyleSheet("QPushButton:checked {background: rgba(255,255,255,1); border: 2px solid #888} \
			QPushButton{background: rgba(255,255,255,0); outline: none;}")

    def changeText(self, label, text):
        tmp = QtWidgets.QApplication.translate(
            "TemperatureWindow", label.format[0]+text+label.format[1], None, -1)
        label.setText(tmp)
