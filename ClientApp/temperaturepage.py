from builtins import str

import math
import traceback
import pprint
import logging

import PyQt5.QtCore
from PyQt5.QtCore import Qt, pyqtSignal

from constants import *
from .qt.temperaturepage_qt import Ui_TemperaturePage
from .notactiveprint_wid import NotActivePrintWidget
from .activeprint_wid import ActivePrintWidget
from .runout_handler import RunoutHandlerDialog
from .timehandler import TimeHandler
from .preheatmaterial import Material
from .periph import Periph
from .printhandler import PrintHandler

from .printer_if import PrinterIF
from .basepage import BasePage
from .tempolcontrol import TempOLControl, TempUIContext
from .util.temputils import break_up_temperature_struct

from PyQt5 import QtCore, QtGui, QtWidgets


class TemperaturePage(BasePage, Ui_TemperaturePage):

    progress_signal = pyqtSignal(str)

    def __init__(self, context):
        super(TemperaturePage, self).__init__()

        # Set up the UI
        self.setupUi(self)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("TemperaturePage __init__")

        self.context = context
        self.printer_if = context.printer_if
        self.ui_controller = context.ui_controller

        self.ActivePrintWid = ActivePrintWidget(self)
        self.NotActivePrintWid = NotActivePrintWidget(self)
        self.w_runout_handler = RunoutHandlerDialog(self, self.printer_if)

        self.gridLayout.addWidget(self.NotActivePrintWid, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.ActivePrintWid, 2, 0, 1, 1)

        self.notactiveprint()
        # self.activeprint()

        self.progress_signal.connect(self.update_progress_slot)

        # self.printer_if.set_temperature_callback(self)
        self.printer_if.temperature_change_connector().register(self.update_temperatures)
        self.printer_if.position_connector().register(self.update_position)

        # self.printer_if.set_printer_state_callback(self)
        # self.printer_if.set_position_callback(self)
        self.printer_if.set_progress_callback(self)

        self.setAllStyleProperty([self.e0temp, self.e1temp, self.bedtemp,
                                  self.w_label_extruder0_setpoint, self.w_label_extruder1_setpoint, self.w_label_bed_setpoint],
                                 "black-transparent-text font-m")

        self.w_label_extruder0_setpoint.setText('0')
        self.w_label_extruder1_setpoint.setText('0')
        self.w_label_bed_setpoint.setText('0')

        self.setAllTransparentIcon([self.e0img, self.e1img, self.bedimg])

        self.setAllTransparentButton([self.w_pushbutton_extruder0_decrement, self.w_pushbutton_extruder0_increment,
                                      self.w_pushbutton_extruder1_decrement, self.w_pushbutton_extruder1_increment,
                                      self.w_pushbutton_bed_decrement, self.w_pushbutton_bed_increment])

        extruder0_ui_context = TempUIContext(self.w_label_extruder0_setpoint,
                                             self.w_pushbutton_extruder0_decrement,
                                             self.w_pushbutton_extruder0_increment)
        self.extruder0_olcontrol = TempOLControl(
            context, extruder0_ui_context, "tool0")

        extruder1_ui_context = TempUIContext(self.w_label_extruder1_setpoint,
                                             self.w_pushbutton_extruder1_decrement,
                                             self.w_pushbutton_extruder1_increment)
        self.extruder1_olcontrol = TempOLControl(
            context, extruder1_ui_context, "tool1")

        bed_ui_context = TempUIContext(self.w_label_bed_setpoint,
                                       self.w_pushbutton_bed_decrement,
                                       self.w_pushbutton_bed_increment)
        self.bed_olcontrol = TempOLControl(context, bed_ui_context, "bed")

        #self.extruder2 = Periph("Extruder 1", "e2", self.set_tool1_temperature, 345, self)
        #self.heatedbed = Periph("Bed", "bed", self.set_bed_temperature, 125, self)

        self.m0 = Material("PLA", self.extruder0_olcontrol,
                           self.extruder1_olcontrol, self.bed_olcontrol, 180, 180, 60)
        self.m1 = Material("PC", self.extruder0_olcontrol,
                           self.extruder1_olcontrol, self.bed_olcontrol, 215, 215, 115)
        self.m2 = Material("PETG", self.extruder0_olcontrol,
                           self.extruder1_olcontrol, self.bed_olcontrol, 200, 200, 60)
        self.cooldown = Material("cooldown", self.extruder0_olcontrol,
                                 self.extruder1_olcontrol, self.bed_olcontrol, 0, 0, 0)

#		Dynamic Icons
        self.fanon = False
        self.fanofficon = QtGui.QIcon()
        self.fanofficon.addPixmap(QtGui.QPixmap(
            ":/img/img/Fans_off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fanonicon = QtGui.QIcon()
        self.fanonicon.addPixmap(QtGui.QPixmap(
            ":/img/img/Fans.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.unheated = QtGui.QIcon()
        self.bedheated1 = QtGui.QIcon()
        self.unheated.addPixmap(QtGui.QPixmap(
            ":/img/img/Bed.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bedheated1.addPixmap(QtGui.QPixmap(
            ":/img/img/Heated_Bed.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

#		Initilization for Not-Printing Widget.
        self.setStyleProperty(self.NotActivePrintWid.BottomBar, "bottom-bar")
        self.NotActivePrintWid.Back.clicked.connect(self.back)
        self.initpreheatbuttons()
        # self.NotActivePrintWid.w_pushbutton_cooldown.clicked.connect(self.notactive_cool)
        self.NotActivePrintWid.w_pushbutton_fan.clicked.connect(
            self.notactive_fan)
        self.setAllStyleProperty([self.NotActivePrintWid.PreheatPLA, self.NotActivePrintWid.PreheatPC, self.NotActivePrintWid.PreheatPETG],
                                 "black-transparent-text font-m align-center")
        self.setAllTransparentButton(
            [self.NotActivePrintWid.Back, self.NotActivePrintWid.w_pushbutton_fan, self.NotActivePrintWid.w_pushbutton_cooldown], True)


#		Initilization for Printing Widget.
        self.setStyleProperty(self.ActivePrintWid.BottomBar, "bottom-bar")
        self.ActivePrintWid.Back.clicked.connect(self.back)
        self.ActivePrintWid.w_pushbutton_fan.clicked.connect(self.active_fan)
        self.ActivePrintWid.w_pushbutton_pauseprint.setEnabled(False)

        # self.ActivePrintWid.StopPrint.clicked.connect(self.stopprint)
        self.ActivePrintWid.w_pushbutton_pauseprint.clicked.connect(
            self.pauseprint)
        self.ActivePrintWid.w_pushbutton_resumeprint.clicked.connect(
            self.resumeprint)
        self.ActivePrintWid.w_pushbutton_flowrate.clicked.connect(
            self.handle_flowratelabel_touch)
        self.ActivePrintWid.w_pushbutton_flowrate_inc.clicked.connect(
            self.flowrate_inc)
        self.ActivePrintWid.w_pushbutton_flowrate_dec.clicked.connect(
            self.flowrate_dec)
        self.ActivePrintWid.w_pushbutton_babystep_dec.clicked.connect(
            self.babystepneg)
        self.ActivePrintWid.w_pushbutton_babystep_inc.clicked.connect(
            self.babysteppos)
        self.ActivePrintWid.w_slider_feedrate.valueChanged.connect(
            self.feedrateslider_changed)
        self.ActivePrintWid.w_slider_feedrate.sliderReleased.connect(
            self.feedrateslider_released)

        # self.ActivePrintWid.FlowrateLabel.
        self.setAllStyleProperty([self.ActivePrintWid.w_label_filename, self.ActivePrintWid.w_label_flowrate, self.ActivePrintWid.w_label_feedrate,
                                  self.ActivePrintWid.w_label_babystep_val], "black-transparent-text font-m")
        self.setStyleProperty(
            self.ActivePrintWid.w_label_position, "white-transparent-text font-l")
        self.setAllStyleProperty([self.ActivePrintWid.w_label_file, self.ActivePrintWid.w_pushbutton_feedrate,
                                  self.ActivePrintWid.w_pushbutton_flowrate, self.ActivePrintWid.w_pushbutton_babystep], "btn-font-l transparent-btn")

        self.setAllTransparentButton([self.ActivePrintWid.w_pushbutton_flowrate_inc, self.ActivePrintWid.w_pushbutton_flowrate_dec,
                                      self.ActivePrintWid.w_pushbutton_babystep_inc, self.ActivePrintWid.w_pushbutton_babystep_dec])
        self.setAllTransparentButton([self.ActivePrintWid.Back, self.ActivePrintWid.w_pushbutton_pauseprint,
                                      self.ActivePrintWid.w_pushbutton_resumeprint, self.ActivePrintWid.w_pushbutton_fan], True)
        self.time_handler = TimeHandler(self, self.bed_olcontrol)
        self.time_handler.start()

        self.print_handler = PrintHandler(self.context, self)

        self.control_page = self.ui_controller.get_page(k_control_page)

    def update_parameter_display(self):
        self._log("update_paramater_display")

        print_page = self.ui_controller.get_page(k_print_page)
        if print_page is not None:
            file_being_printed = print_page.file_being_printed
            self.ActivePrintWid.w_label_filename.setText(
                str(file_being_printed))

        self.ActivePrintWid.w_label_feedrate.setText(
            str(self.print_handler.feedrate))
        self.ActivePrintWid.w_label_babystep_val.setText(
            str(self.print_handler.babystep))
        self.ActivePrintWid.w_slider_feedrate.setValue(
            self.print_handler.feedrate)
        self.updateflowlabel()

    def reset_parameters(self):
        self._log("***************************************************************************************************reset_paramaters")
        self.print_handler.reset_parameters()
        self.print_handler.send_all()
        self.update_parameter_display()

    def feedrateslider_released(self):
        self._log("UI: User released Feed Rate slider")

        feed_rate = self.ActivePrintWid.w_slider_feedrate.value()
        indicated_feed_rate = feed_rate

        if feed_rate < 50:
            feed_rate = 50

        if feed_rate > 200:
            feed_rate = 200

        if feed_rate != indicated_feed_rate:
            self.ActivePrintWid.w_slider_feedrate.setValue(feed_rate)

        self.print_handler.feedrate = feed_rate
        self.print_handler.sendfeedrate()

    def feedrateslider_changed(self):
        self._log("UI: User moved Feed Rate slider")
        val = self.ActivePrintWid.w_slider_feedrate.value()
        self.ActivePrintWid.w_label_feedrate.setText(str(val))

    def babystepneg(self):
        self._log("UI: User touched Baby Step Decrement")
        self.print_handler.babystepx10 -= self.print_handler.babystepinc
        self.print_handler.babystep = float(
            self.print_handler.babystepx10) / float(100)
        self.ActivePrintWid.w_label_babystep_val.setText(
            str(self.print_handler.babystep))
        # self.print_handler.sendbabystep()
        self.printer_if.set_babystep(self.print_handler.babystep)

    def babysteppos(self):
        self._log("UI: User touched Baby Step Increment")
        self.print_handler.babystepx10 += self.print_handler.babystepinc
        self.print_handler.babystep = float(
            self.print_handler.babystepx10) / float(100)
        self.ActivePrintWid.w_label_babystep_val.setText(
            str(self.print_handler.babystep))
        # self.print_handler.sendbabystep()
        self.printer_if.set_babystep(self.print_handler.babystep)

    def updateposition(self, x, y, z):

        # pos = self.serial.data.position
        pos = 0

        # Compute the values to display. Display X and Y as integers,
        # but Z as a decimal.
        x = int(math.floor(float(x)))
        y = int(math.floor(float(y)))
        z = float(z)

        position_string = "X: %1.2f Y: %1.2f Z: %1.2f" % (x, y, z)

        self.ActivePrintWid.w_label_position.setText(position_string)
        self.control_page.PositionLabel.setText(position_string)

    def update_progress(self, completion, print_time_left):
        self.progress_signal.emit(str(completion))

    def update_progress_slot(self, completion):
        if completion != "N/A":
            self._log("Received progress signal <%s>" % completion)
            completion = int(float(completion))
            self.ActivePrintWid.w_progressbar_file_progress.setValue(
                completion)

    def updateflowlabel(self):
        flow_button_text = "Flowrate: " + \
            self.print_handler.fr_text[self.print_handler.fr_index]
        self.ActivePrintWid.w_pushbutton_flowrate.setText(flow_button_text)
        self.ActivePrintWid.w_label_flowrate.setText(
            str(self.print_handler.flowrate[self.print_handler.fr_index]))

    def handle_flowratelabel_touch(self):

        self._log("UI: User touched Flow Rate Label")

        # Increment the flow rate index, cycling between ALL, Extruder
        # 0, and Extruder 1
        self.print_handler.fr_index = (self.print_handler.fr_index + 1) % 3

        self.updateflowlabel()

    def flowrate_inc(self):
        self._log("UI: User touched Flow Rate Increase")
        self.flowrateadjust(+1)

    def flowrate_dec(self):
        self._log("UI: User touched Flow Rate Increase")
        self.flowrateadjust(-1)

    def flowrateadjust(self, amount):
        self._log("UI: User touched Flow Rate Decrease")

        # Decrease the flow rate
        self.print_handler.flowrate[self.print_handler.fr_index] += amount

        # Limit the flow rate to be at least 75:
        if self.print_handler.flowrate[self.print_handler.fr_index] < 75:
            self.print_handler.flowrate[self.print_handler.fr_index] = 75

        # Limit the flow rate to be at most 150:
        if self.print_handler.flowrate[self.print_handler.fr_index] > 125:
            self.print_handler.flowrate[self.print_handler.fr_index] = 125

        # self.printer_if.set_flow_rate(self.print_handler.flowrate[self.print_handler.fr_index])
        self.print_handler.sendflowrate()
        self.updateflowlabel()

    def notactiveprint(self):
        # self.NotActivePrintWid.show()
        # self.ActivePrintWid.hide()
        self.NotActivePrintWid.setVisible(True)
        self.ActivePrintWid.setVisible(False)

    def activeprint(self):
        # self.NotActivePrintWid.hide()
        self.ActivePrintWid.w_pushbutton_resumeprint.setEnabled(False)
        self.ActivePrintWid.w_pushbutton_pauseprint.setEnabled(True)
        # self.ActivePrintWid.show()
        self.NotActivePrintWid.setVisible(False)
        self.ActivePrintWid.setVisible(True)

    def pauseprint(self):
        self._log("UI: User touched Pause")
        self.printer_if.pause_print()
        self.ActivePrintWid.w_pushbutton_resumeprint.setEnabled(True)
        self.ActivePrintWid.w_pushbutton_pauseprint.setEnabled(False)
        # self.parent.Control.setEnabled(True)
        home = self.ui_controller.get_page(k_home_page)
        home.pushbutton_control.setEnabled(True)

    def resumeprint(self):
        self._log("UI: User touched Resume")
        self.printer_if.resume_print()
        self.ActivePrintWid.w_pushbutton_resumeprint.setEnabled(False)
        self.ActivePrintWid.w_pushbutton_pauseprint.setEnabled(True)
        # self.parent.Control.setEnabled(False)
        home = self.ui_controller.get_page(k_home_page)
        home.pushbutton_control.setEnabled(False)

    def initpreheatbuttons(self):
        self.setAllTransparentButton([self.NotActivePrintWid.w_pushbutton_m0_extruder0, self.NotActivePrintWid.w_pushbutton_m0_extruder1, self.NotActivePrintWid.w_pushbutton_m0_bed, self.NotActivePrintWid.w_pushbutton_m0_all,
                                      self.NotActivePrintWid.w_pushbutton_m1_extruder0, self.NotActivePrintWid.w_pushbutton_m1_extruder1, self.NotActivePrintWid.w_pushbutton_m1_bed, self.NotActivePrintWid.w_pushbutton_m1_all,
                                      self.NotActivePrintWid.w_pushbutton_m2_extruder0, self.NotActivePrintWid.w_pushbutton_m2_extruder1, self.NotActivePrintWid.w_pushbutton_m2_bed, self.NotActivePrintWid.w_pushbutton_m2_all])

        self.NotActivePrintWid.w_pushbutton_m0_extruder0.clicked.connect(
            self.m0.e0set)
        self.NotActivePrintWid.w_pushbutton_m0_extruder1.clicked.connect(
            self.m0.e1set)
        self.NotActivePrintWid.w_pushbutton_m0_bed.clicked.connect(
            self.m0.bedset)
        self.NotActivePrintWid.w_pushbutton_m0_all.clicked.connect(
            self.m0.allset)

        self.NotActivePrintWid.w_pushbutton_m1_extruder0.clicked.connect(
            self.m1.e0set)
        self.NotActivePrintWid.w_pushbutton_m1_extruder1.clicked.connect(
            self.m1.e1set)
        self.NotActivePrintWid.w_pushbutton_m1_bed.clicked.connect(
            self.m1.bedset)
        self.NotActivePrintWid.w_pushbutton_m1_all.clicked.connect(
            self.m1.allset)

        self.NotActivePrintWid.w_pushbutton_m2_extruder0.clicked.connect(
            self.m2.e0set)
        self.NotActivePrintWid.w_pushbutton_m2_extruder1.clicked.connect(
            self.m2.e1set)
        self.NotActivePrintWid.w_pushbutton_m2_bed.clicked.connect(
            self.m2.bedset)
        self.NotActivePrintWid.w_pushbutton_m2_all.clicked.connect(
            self.m2.allset)

        self.NotActivePrintWid.w_pushbutton_cooldown.clicked.connect(
            self.cooldown.allset)

    def notactive_fan(self):
        self._log("UI: User touched (not active) Fan")
        self.fan()

    def active_fan(self):
        self._log("UI: User touched (active) Fan")
        self.fan()

    def fan(self):
        if self.fanon:
            self.fanon = False
            self.printer_if.fans_off()
            self.ActivePrintWid.w_pushbutton_fan.setIcon(self.fanofficon)
            self.ActivePrintWid.w_pushbutton_fan.setIconSize(
                QtCore.QSize(55, 55))
            self.NotActivePrintWid.w_pushbutton_fan.setIcon(self.fanofficon)
            self.NotActivePrintWid.w_pushbutton_fan.setIconSize(
                QtCore.QSize(55, 55))
        elif not self.fanon:
            self.fanon = True
            self.printer_if.fans_on()
            self.ActivePrintWid.w_pushbutton_fan.setIcon(self.fanonicon)
            self.ActivePrintWid.w_pushbutton_fan.setIconSize(
                QtCore.QSize(55, 55))
            self.NotActivePrintWid.w_pushbutton_fan.setIcon(self.fanonicon)
            self.NotActivePrintWid.w_pushbutton_fan.setIconSize(
                QtCore.QSize(55, 55))

    def active_close(self):
        self._log("UI: User touched (active) Back")
        self.parent.show()
        self.close()

    def notactive_close(self):
        self._log("UI: User touched (not active) Back")
        self.parent.show()
        self.close()

    def update_position(self, xyz_tuple):
        (x, y, z) = xyz_tuple
        self.updateposition(x, y, z)

    def update_printer_state(self, data):
        print("PRINTER STATE CHANGE", data)

    def update_temperatures(self, temps_tuple):

        # Separate temps into the three tuples
        (bed_tuple, tool0_tuple, tool1_tuple) = temps_tuple

        unknown_temp_str = "----"

        # Heated bed

        # break up the tuple containing the target and actual temperatures
        (bed_target_temp, bed_actual_temp) = bed_tuple

        if bed_actual_temp is not None:
            self.bedtemp.setText(str(int(bed_actual_temp + 0.5)))
        else:
            self.bedtemp.setText(unknown_temp_str)

        # Extruder 0

        # break up the tuple containing the target and actual temperatures
        (tool0_target_temp, tool0_actual_temp) = tool0_tuple

        if tool0_actual_temp is not None:
            self.e0temp.setText(str(int(tool0_actual_temp + 0.5)))
        else:
            self.e0temp.setText(unknown_temp_str)

        # Extruder 1

        # break up the tuple containing the target and actual temperatures
        (tool1_target_temp, tool1_actual_temp) = tool1_tuple

        if tool1_actual_temp is not None:
            self.e1temp.setText(str(int(tool1_actual_temp + 0.5)))
        else:
            self.e1temp.setText(unknown_temp_str)

    def set_bed_temperature(self, value):
        self._log("Setting bed temp to %d." % value)
        self.printer_if.set_temperature("bed", value)

    def set_tool0_temperature(self, value):
        self._log("Setting tool0 temp to %d." % value)
        self.printer_if.set_temperature("tool0", value)

    def set_tool1_temperature(self, value):
        self._log("Setting tool1 temp to %d." % value)
        self.printer_if.set_temperature("tool1", value)

    def set_progress(self, value):
        pass
