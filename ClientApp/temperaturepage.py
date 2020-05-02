from builtins import str

import math
import traceback
import pprint
import logging

import PyQt5.QtCore
from PyQt5.QtCore import Qt, pyqtSignal

from constants import *
from .qt.temperaturepage_qt import Ui_TemperaturePage
from .notactiveprint_wid import *
from .activeprint_wid import *
from .runout_handler import RunoutHandlerDialog
from .event_hand import *
from .preheatmaterial import *
from .periph import *

from .printer_if import PrinterIF
from .basepage import BasePage

from PyQt5 import QtCore, QtGui, QtWidgets

mats = [('PLA', 'm1'),
        ('PC', 'm2'),
        ('PETG', 'm3')]

periphs = ['e1', 'e2', 'bed', 'all']


class TemperaturePage(BasePage, Ui_TemperaturePage):

    progress_signal = pyqtSignal(str)

    def __init__(self, context):
        super(TemperaturePage, self).__init__()

        # Set up the UI
        self.setupUi(self)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("TemperaturePage __init__")

        # if parent.fullscreen: self.fullscreen = True
        # else: self.fullscreen = False
        # if self.fullscreen:
        # 	self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        self.printer_if = context.printer_if
        self.ui_controller = context.ui_controller

        self.event_handler = event_handler()

        self.ActivePrintWid = ActivePrintWidget(self)
        self.NotActivePrintWid = NotActivePrintWidget(self)
        self.w_runout_handler = RunoutHandlerDialog(self, self.printer_if)

        self.gridLayout.addWidget(self.NotActivePrintWid, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.ActivePrintWid, 2, 0, 1, 1)

        self.notactiveprint()
        self.pushbutton_back.clicked.connect(self.back)

        # self.serial.data.updateprogress.connect(self.updateprogress)
        # self.serial.data.updateposition.connect(self.updateposition)

        # self.event_handler.updatetemperatures.connect(self.updatetemperatures)
        self.progress_signal.connect(self.update_progress_slot)

        self.printer_if.set_temperature_callback(self)
        self.printer_if.set_printer_state_callback(self)
        self.printer_if.set_position_callback(self)
        self.printer_if.set_progress_callback(self)
        
        self.inittextformat(self.e1temp)
        self.inittextformat(self.e2temp)
        self.inittextformat(self.bedtemp)
        self.inittextformat(self.e1set)
        self.inittextformat(self.e2set)
        self.inittextformat(self.bedset)
        self.changeText(self.e1set, '0')
        self.changeText(self.e2set, '0')
        self.changeText(self.bedset, '0')

        self.setbuttonstyle(self.e1img)
        self.setbuttonstyle(self.e2img)
        self.setbuttonstyle(self.bedimg)

        self.extruder1 = Periph("Extruder 0", "e1", self.set_tool0_temperature, 345, self)
        self.extruder2 = Periph("Extruder 1", "e2", self.set_tool1_temperature, 345, self)
        self.heatedbed = Periph("Bed", "bed", self.set_bed_temperature, 125, self)

        self.m1 = Material("PLA", 180, 180, 60, self)
        self.m2 = Material("PC", 215, 215, 115, self)
        self.m3 = Material("PETG", 200, 200, 60, self)

#		Dynamic Icons
        self.fanon = False
        self.fanofficon = QtGui.QIcon()
        self.fanofficon.addPixmap(QtGui.QPixmap(
            "img/fanoff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fanonicon = QtGui.QIcon()
        self.fanonicon.addPixmap(QtGui.QPixmap(
            "img/fanon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.unheated = QtGui.QIcon()
        self.bedheated1 = QtGui.QIcon()
        self.bedheated2 = QtGui.QIcon()
        self.unheated.addPixmap(QtGui.QPixmap(
            "img/bed_unheated.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bedheated1.addPixmap(QtGui.QPixmap(
            "img/bed_heated1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bedheated2.addPixmap(QtGui.QPixmap(
            "img/bed_heated2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)


#		Initilization for Not-Printing Widget.

        self.initpreheatbuttons()
        self.NotActivePrintWid.CoolDown.clicked.connect(self.notactive_cool)
        self.NotActivePrintWid.Fan.clicked.connect(self.notactive_fan)


#		Initilization for Printing Widget.

        self.ActivePrintWid.Fan.clicked.connect(self.active_fan)
        self.ActivePrintWid.ResumePrint.setEnabled(False)

        # self.ActivePrintWid.StopPrint.clicked.connect(self.stopprint)
        self.ActivePrintWid.PausePrint.clicked.connect(self.pauseprint)
        self.ActivePrintWid.ResumePrint.clicked.connect(self.resumeprint)
        self.ActivePrintWid.FlowrateLabel.clicked.connect(self.flowratelabel)
        self.ActivePrintWid.FlowratePos.clicked.connect(self.flowratepos)
        self.ActivePrintWid.FlowrateNeg.clicked.connect(self.flowrateneg)
        self.ActivePrintWid.BabysteppingNeg.clicked.connect(self.babystepneg)
        self.ActivePrintWid.BabysteppingPos.clicked.connect(self.babysteppos)
        self.ActivePrintWid.FeedrateSlider.valueChanged.connect(
            self.feedrateslider)
        self.ActivePrintWid.FeedrateSlider.sliderReleased.connect(
            self.sendfeedrate)

        # self.ActivePrintWid.FlowrateLabel.
        self.inittextformat(self.ActivePrintWid.FileName)
        self.inittextformat(self.ActivePrintWid.FlowrateVal)
        self.inittextformat(self.ActivePrintWid.FeedrateVal)
        self.inittextformat(self.ActivePrintWid.BabysteppingVal)
        self.inittextformat(self.ActivePrintWid.PositionLabel)

#        self.setbuttonstyle(self.pushbutton_back)
        self.setbuttonstyle(self.ActivePrintWid.FileLabel)
        self.setbuttonstyle(self.ActivePrintWid.FeedrateLabel)
        self.setbuttonstyle(self.ActivePrintWid.BabysteppingLabel)

    def update_parameters(self):
        self.event_handler.resetparameters()

        self.changeText(self.ActivePrintWid.FileName, self.printer_if.file_name)
        self.changeText(self.ActivePrintWid.FeedrateVal, str(self.printer_if.feed_rate))
        self.changeText(self.ActivePrintWid.BabysteppingVal, str(self.event_handler.babystep))
        self.changeText(self.ActivePrintWid.FlowrateVal, str(self.printer_if.flow_rate))

    def sendfeedrate(self):
        self._log("UI: User released Feed Rate slider")

        feed_rate = self.ActivePrintWid.FeedrateSlider.value()
        indicated_feed_rate = feed_rate

        if feed_rate < 50:
            feed_rate = 50

        if feed_rate > 200:
            feed_rate = 200

        if feed_rate != indicated_feed_rate:
            self.ActivePrintWid.FeedrateSlider.setValue(feed_rate)

        self.printer_if.set_feed_rate(self.ActivePrintWid.FeedrateSlider.value())

        # self.serial.send_serial(
        #     "M220 S" + str(self.ActivePrintWid.FeedrateSlider.value()))
        pass

    def feedrateslider(self):
        self._log("UI: User moved Feed Rate slider")
        val = self.ActivePrintWid.FeedrateSlider.value()
        self.changeText(self.ActivePrintWid.FeedrateVal, str(val))

    def babystepneg(self):
        self._log("UI: User touched Baby Step Decrement")
        self.event_handler.babystepx10 -= self.event_handler.babystepinc
        self.event_handler.babystep = float(
            self.event_handler.babystepx10) / float(100)
        self.changeText(self.ActivePrintWid.BabysteppingVal,
                        str(self.event_handler.babystep))
        # self.event_handler.sendbabystep()
        self.printer_if.set_babystep(self.event_handler.babystep)

    def babysteppos(self):
        self._log("UI: User touched Baby Step Increment")
        self.event_handler.babystepx10 += self.event_handler.babystepinc
        self.event_handler.babystep = float(
            self.event_handler.babystepx10) / float(100)
        self.changeText(self.ActivePrintWid.BabysteppingVal,
                        str(self.event_handler.babystep))
        # self.event_handler.sendbabystep()
        self.printer_if.set_babystep(self.event_handler.babystep)

    def updateposition(self, x, y, z):

        # pos = self.serial.data.position
        pos = 0

        # Compute the values to display. Display X and Y as integers,
        # but Z as a decimal.
        x = int(math.floor(float(x)))
        y = int(math.floor(float(y)))
        z = float(z)

        position_string = "X: %d Y: %d Z:%1.2f" % (x, y, z)

        self.changeText(self.ActivePrintWid.PositionLabel, position_string)

    def update_progress(self, completion, print_time_left):
        self.progress_signal.emit(str(completion))

    def update_progress_slot(self, completion):

        if completion != "N/A":
            self._log("Received progress signal <%s>" % completion)
            completion = int(float(completion))
            self.ActivePrintWid.FileProgress.setValue(completion)

    def updateflowlabel(self):
        flow_button_text = "Flowrate: " + \
            self.event_handler.fr_text[self.event_handler.fr_index]
        self.ActivePrintWid.FlowrateLabel.setText(flow_button_text)
        self.changeText(self.ActivePrintWid.FlowrateVal, str(
            self.event_handler.flowrate[self.event_handler.fr_index]))

    def flowratelabel(self):
        # Select the next of the three:
        # self.event_handler.fr_index = (self.event_handler.fr_index + 1) % 3
        self._log("UI: User touched Flow Rate Label")
        self.updateflowlabel()

    def flowratepos(self):
        self._log("UI: User touched Flow Rate Increase")

        # Increase the flow rate
        self.event_handler.flowrate[self.event_handler.fr_index] += 1

        # Limit the flow rate to be at most 150:
        if self.event_handler.flowrate[self.event_handler.fr_index] > 125:
            self.event_handler.flowrate[self.event_handler.fr_index] = 125

        self.printer_if.set_flow_rate(self.event_handler.flowrate[self.event_handler.fr_index])
        # self.event_handler.sendflowrate()
        self.updateflowlabel()

    def flowrateneg(self):
        self._log("UI: User touched Flow Rate Decrease")

        # Decrease the flow rate
        self.event_handler.flowrate[self.event_handler.fr_index] -= 1

        # Limit the flow rate to be at least 75:
        if self.event_handler.flowrate[self.event_handler.fr_index] < 75:
            self.event_handler.flowrate[self.event_handler.fr_index] = 75

        self.printer_if.set_flow_rate(self.event_handler.flowrate[self.event_handler.fr_index])
        # self.event_handler.sendflowrate()
        self.updateflowlabel()

    def activeprint(self):
        self.NotActivePrintWid.hide()
        self.ActivePrintWid.ResumePrint.setEnabled(False)
        self.ActivePrintWid.PausePrint.setEnabled(True)
        self.ActivePrintWid.show()

    def pauseprint(self):
        self._log("UI: User touched Pause")
        self.printer_if.pause_print()
        self.ActivePrintWid.ResumePrint.setEnabled(True)
        self.ActivePrintWid.PausePrint.setEnabled(False)
        #self.parent.Control.setEnabled(True)
        home = self.ui_controller.get_page(k_home_page)
        home.pushbutton_control.setEnabled(True)

    def resumeprint(self):
        self._log("UI: User touched Resume")
        self.printer_if.resume_print()
        self.ActivePrintWid.ResumePrint.setEnabled(False)
        self.ActivePrintWid.PausePrint.setEnabled(True)
        #self.parent.Control.setEnabled(False)
        home = self.ui_controller.get_page(k_home_page)
        home.pushbutton_control.setEnabled(False)

    def notactiveprint(self):
        self.NotActivePrintWid.show()
        self.ActivePrintWid.hide()

    # def stopprint(self):
    # 	self.serial.reset()
    # 	self.parent.print_pop.cancelled()
    # 	self.serial.data.resetsettemps()

    # def initposnegbuttons(self):
    # 	for p in periphs:
    # 		if p == "all": continue
    # 		setattr(self,p+ "timer", QTimer())
    # 		getattr(self, p+ "pos").clicked.connect(getattr(self.event_handler, "increment_"+p))
    # 		getattr(self, p+ "neg").clicked.connect(getattr(self.event_handler, "decrement_"+p))

    def initpreheatbuttons(self):
        for name, m in mats:
            for p in periphs:
                getattr(self.NotActivePrintWid, m + p).clicked.connect(getattr(getattr(self, m), p + 'set'))

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
            self.ActivePrintWid.Fan.setIcon(self.fanofficon)
            self.ActivePrintWid.Fan.setIconSize(QtCore.QSize(55, 55))
            self.NotActivePrintWid.Fan.setIcon(self.fanofficon)
            self.NotActivePrintWid.Fan.setIconSize(QtCore.QSize(55, 55))
        elif not self.fanon:
            self.fanon = True
            self.printer_if.fans_on()
            self.ActivePrintWid.Fan.setIcon(self.fanonicon)
            self.ActivePrintWid.Fan.setIconSize(QtCore.QSize(55, 55))
            self.NotActivePrintWid.Fan.setIcon(self.fanonicon)
            self.NotActivePrintWid.Fan.setIconSize(QtCore.QSize(55, 55))

    def active_close(self):
        self._log("UI: User touched (active) Back")
        self.parent.show()
        self.close()

    def notactive_close(self):
        self._log("UI: User touched (not active) Back")
        self.parent.show()
        self.close()

    def notactive_cool(self):
        self._log("UI: User touched Cooldown")
        self.extruder1.setandsend(0)
        self.extruder2.setandsend(0)
        self.heatedbed.setandsend(0)

    def update_position(self, x, y, z):
        self.updateposition(x, y, z)

    def update_printer_state(self, data):
        print("PRINTER STATE CHANGE", data)

    def update_temperatures(self, data):

        # Get the tuple of tuples by breaking up the data struct
        temps_tuple = self._break_up_temperature_struct(data)

        # self.pp.pprint(temps_tuple)

        # Separate temps into the three tuples
        (bed_tuple, tool0_tuple, tool1_tuple) = temps_tuple

        unknown_temp_str = "----"

        ### Heated bed

        # break up the tuple containing the target and actual temperatures
        (bed_target_temp, bed_actual_temp) = bed_tuple

        if bed_actual_temp is not None:
            # print("bed target %d, bed actual %d." % (bed_target_temp, bed_actual_temp))

            # Display the temperatures on the UI
            self.changeText(self.bedtemp, str(int(bed_actual_temp + 0.5)))
            self.changeText(self.bedset, str(int(bed_target_temp + 0.5)))

            # And change the set-temperature in the bed periph
            if (self.heatedbed.settemp != bed_target_temp):
                self.heatedbed._set(bed_target_temp)
        else:
            self.changeText(self.bedtemp, unknown_temp_str)
            self.changeText(self.bedset, unknown_temp_str)

        ### Extruder 0

        # break up the tuple containing the target and actual temperatures
        (tool0_target_temp, tool0_actual_temp) = tool0_tuple

        if tool0_actual_temp is not None:
            # print("tool0 target %d, tool0 actual %d." % (tool0_target_temp, tool0_actual_temp))

            # Display the temperatures on the UI.
            self.changeText(self.e1temp, str(int(tool0_actual_temp + 0.5)))
            self.changeText(self.e1set, str(int(tool0_target_temp + 0.5)))

            if (self.extruder1.settemp != tool0_target_temp):
                self.extruder1._set(tool0_target_temp)
        else:
            self.changeText(self.e1temp, unknown_temp_str)
            self.changeText(self.e1set, unknown_temp_str)

        ### Extruder 1

        # break up the tuple containing the target and actual temperatures
        (tool1_target_temp, tool1_actual_temp) = tool1_tuple

        if (tool1_actual_temp is not None) and (tool1_target_temp is not None):
            # print("tool1 target %d, tool1 actual %d." % (tool1_target_temp, tool1_actual_temp))
        
            # Display the temperatures on the UI.
            self.changeText(self.e2temp, str(int(tool1_actual_temp + 0.5)))
            self.changeText(self.e2set, str(int(tool1_target_temp + 0.5)))

            if (self.extruder2.settemp != tool1_target_temp):
                self.extruder2._set(tool1_target_temp)

        else:
            self.changeText(self.e2temp, unknown_temp_str)
            self.changeText(self.e2set, unknown_temp_str)


    def set_bed_temperature(self, value):
        self._log("Setting bed temp to %d." % value)
        self.printer_if.set_temperature("bed", value)

    def set_tool0_temperature(self, value):
        self._log("Setting tool0 temp to %d." % value)
        self.printer_if.set_temperature("tool0", value)
        
    def set_tool1_temperature(self, value):
        self._log("Setting tool1 temp to %d." % value)
        self.printer_if.set_temperature("tool1", value)
        
    def _break_up_temperature_struct(self, data):

        ### Heated bed
        try:
            # Get the dictionary of bed temperatures and from it
            # extract the target and actual temperatures.

            # We have to do this inside an exception handler because
            # sometimes the data dictionary doesn't have bed
            # temperatures inside it (have seen this at startup
            # sometimes).
            bed_temp_dict = data["bed"]
            bed_target_temp = bed_temp_dict["target"]
            bed_actual_temp = bed_temp_dict["actual"]

            # Gather the bed temperatuse into a tuple
            bed_tuple = (bed_target_temp, bed_actual_temp)
            
        except:
            # Don't do anything (but also don't crash)
            bed_tuple = (None, None)

        ### Extruder 0

        try:
            # Get the dictionary of extruder-0 temperatures and from it
            # extract the target and actual temperatures.
            tool0_temp_dict = data["tool0"]
            tool0_target_temp = tool0_temp_dict["target"]
            tool0_actual_temp = tool0_temp_dict["actual"]

            # Gather the tool0 temperatuse into a tuple
            tool0_tuple = (tool0_target_temp, tool0_actual_temp)
        except:
            tool0_tuple = (None, None)

        ### Extruder 1

        try:
            # Get the dictionary of extruder-1 temperatures and from it
            # extract the target and actual temperatures.
            tool1_temp_dict = data["tool1"]
            tool1_target_temp = tool1_temp_dict["target"]
            tool1_actual_temp = tool1_temp_dict["actual"]

            # Gather the tool1 temperatuse into a tuple
            tool1_tuple = (tool1_target_temp, tool1_actual_temp)
        except:
            tool1_tuple = (None, None)

        # Return the broken-apart temperatures as a 3-tuple of 2-tuples
        return (bed_tuple, tool0_tuple, tool1_tuple)
        
    def changeText(self, label, text):
        # tmp = QtWidgets.QApplication.translate(
        #     "TemperaturePage", label.format[0]+text+label.format[1], None, -1)
        label.setText(text)

    def inittextformat(self, label):
        label.format = label.text()
# This line was, prior to converting for python 3:
#		label.format = label.format.encode("utf-8").split("-----")
        label.format = label.format.split("-----")

    def setbuttonstyle(self, obj):
        obj.setStyleSheet(
            "QPushButton{background: rgba(255,255,255,0); outline: none; border: none;}")

    def set_progress(self, value):
        pass