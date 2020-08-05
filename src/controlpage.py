from builtins import str
import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from qt.controlpage_qt import Ui_ControlPage
from axis import Axis
from basepage import BasePage

increments_str = ["01", "1", "10", "100"]
increments_int = ['0.1', '1', '10', '100']


class ControlPage(BasePage, Ui_ControlPage):
    def __init__(self, context):
        super(ControlPage, self).__init__()

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log_d("ControlPage __init__()")

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

        self.setAllTransparentButton([
            self.XPos, self.XNeg,
            self.YPos, self.YNeg,
            self.ZPos, self.ZNeg,
            self.E0Pos, self.E0Neg, self.E1Icon, self.E1Pos, self.E1Neg,
            self.DisableMotors, self.HomeAll, self.HomeXY, self.HomeZ, ])
        self.setAllTransparentButton([self.Back], True)

        self.setAllTransparentIcon([self.XYIcon, self.ZIcon, self.E0Icon, self.E1Icon])


        self.globalIncrementSelector = self.AddButtontoGroup("global")

        self.xaxis = Axis("x", "4500", self, 25)
        self.yaxis = Axis("y", "4500", self, 25)
        self.zaxis = Axis("z", "4500", self, 2)
        self.eaxis = Axis("e0", "60", self)
        self.e1axis = Axis("e1", "60", self)

        # self.serial.data.updateposition.connect(self.updateposition)

        self.HomeXY.clicked.connect(self.homexy)
        self.HomeZ.clicked.connect(self.homez)
        self.HomeAll.clicked.connect(self.homeall)

        self.Back.clicked.connect(self.back)
        self.setStyleProperty(self.BottomBar, "bottom-bar")
        self.setAllStyleProperty([self.xposlabel, self.yposlabel, self.zposlabel,
                                  self.w_lineedit_x_position, self.w_lineedit_y_position, self.w_lineedit_z_position],
                                 "white-transparent-text font-l align-center")

        self.DisableMotors.clicked.connect(self.disablemotors)
        self.Back.clicked.connect(self.user_back)
    def hello(self):
        print("hello")
    def user_back(self):
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
        self._log_d("UI: User touched Motor enable/disable")
        self.printer_if.commands("M18", force=True)
        pass

    def homexy(self):
        # self.serial.send_serial('G28 XY')
        self._log_d("UI: User touched Home XY")
        self.printer_if.homexy()

    def homez(self):
        # self.serial.send_serial('G28 Z')
        self._log_d("UI: User touched Home Z")
        self.printer_if.homez()

    def homeall(self):
        # self.serial.send_serial('G28')
        self._log_d("UI: User touched Home All")
        self.printer_if.homeall()

    def AddButtontoGroup(self, axis):
        group = QtWidgets.QButtonGroup(self)
        for i in increments_str:
            att = axis + "m" + i
            getattr(self, att).setCheckable(True)
            self.setStyleProperty(getattr(self, att),
                                  "btn-font-s yellow-selected-btn transparent-btn black-text")
            group.addButton(getattr(self, att))
        getattr(self, axis + "m"+"10").setChecked(True)
        return group
