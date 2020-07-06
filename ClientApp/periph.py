from builtins import str
from builtins import object

import sys
import logging
import traceback

import PyQt5


class Periph(object):
    def __init__(self, fullname, name, callback, maxtemp, parent):
        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("TemperatureWindow __init__")

        self.fullname = fullname
        self.name = name
        self.callback = callback
        self.maxtemp = maxtemp
        self.parent = parent

        self.timer = PyQt5.QtCore.QTimer()
        self.timer.timeout.connect(self.button_event_check)
        self.button_held_time = 0
        self.direction = "inc"

        self.held_count = 0

        # self.reflect_delay_timer = PyQt5.QtCore.QTimer()
        # self.reflect_delay_timer.timeout.connect(self.reflect_delay_check)
        # self.local_set_time = 0

        self.settemp = 0
        self.external_settemp = 0
        self.has_external_settemp = False

        self.init_posneg()

    def _log(self, message):
        self._logger.debug(message)

    def init_posneg(self):
        getattr(self.parent, self.name +
                "pos").clicked.connect(self.increment)
        getattr(self.parent, self.name +
                "neg").clicked.connect(self.decrement)

        getattr(self.parent, self.name +
                "pos").pressed.connect(self.incrementbuttonpressed)
        getattr(self.parent, self.name +
                "neg").pressed.connect(self.decrementbuttonpressed)

        getattr(self.parent, self.name +
                "pos").released.connect(self.buttonreleased)
        getattr(self.parent, self.name +
                "neg").released.connect(self.buttonreleased)

    def incrementbuttonpressed(self):
        self._log("UI: <%s> Increment button pressed " % self.fullname)
        self.held_count = 0
        self.timer.start(12)
        self.direction = "inc"

    def decrementbuttonpressed(self):
        self._log("UI: <%s> Decrement button pressed " % self.fullname)
        self.held_count = 0
        self.timer.start(12)
        self.direction = "dec"

    def buttonreleased(self):
        if self.held_count > 0:
            self._log("UI: <%s> button released after %d repeats" %
                      (self.fullname, self.held_count))
            self.held_count = 0
        self.timer.stop()
        if (self.button_held_time == 0 and self.direction == "inc"):
            self.increment()
        elif (self.button_held_time == 0 and self.direction == "dec"):
            self.decrement()
        self.sendtemp()
        self.button_held_time = 0

    def button_event_check(self):
        self.button_held_time += 0.012
        self.parent.event_handler.sendtempcount = 0
        if self.button_held_time >= 1:
            self.held_count += 1
            if self.direction == "inc":
                self.increment()
            elif self.direction == "dec":
                self.decrement()

    def increment(self):
        # print("In increment, current settemp = %d." % (self.settemp))
        if self.settemp < self.maxtemp:
            self.settemp += 1
        self.setandsend(self.settemp)

    def decrement(self):
        # print("In decrement, current settemp = %d." % (self.settemp))
        if self.settemp > 0:
            self.settemp -= 1
        self.setandsend(self.settemp)

    def setandsend(self, num):
        # print("In set-and-send")
        self._set(num)
        self.sendtemp()

    def _set(self, num):
        # print("In _set, current settemp = %d, new settemp = %d" % (self.settemp, num))
        # traceback.print_stack()
        self.settemp = num

    def sendtemp(self):
        # print("self.command = %s, overall command = <%s>" % (self.command,
        #                                                      self.command + str(self.settemp)))
        # # traceback.print_stack()

        # print("SETTING temp to %d." % (self.settemp))

        # self.parent.printer_if.commands(self.command + str(self.settemp))
        # self.parent.printer_if.commands("M105")

        # # self.parent.serial.send_serial(self.command + str(self.settemp))
        # # self.parent.serial.send_serial("M105")

        self.callback(self.settemp)
        self.parent.event_handler.sendtempcount = 0

    def set_target_from_external(self, temp):
        self.external_settemp = temp
        self.has_external_settemp = True

    def reflect_delay_check(self):
        pass
