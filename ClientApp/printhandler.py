from builtins import str
import logging

# The Event Handler operates the temperature preheats, setting the temperatures,
#

class PrintHandler():
    def __init__(self, context, tempwindow):
        super(PrintHandler).__init__()

        self.printer_if = context.printer_if
        self.tempwindow = tempwindow

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("TemperaturePage __init__")

        # Feed rate variables
        self.feedrate = 100

        # Flow rate variables
        self.fr_index = 2 # ALL is the default
        self.fr_text = ["E0", "E1", "All"]
        self.flowrate = [100, 100, 100]

        # Babystep variables
        self.babystep = 0
        self.babystepx10 = 0
        self.babystepinc = 1

        self.sendtempcount = 0
        self.rescanserial_count = 0

    def _log(self, message):
        self._logger.debug(message)

    def reset_parameters(self):
        self._log("reset_parameters")
        self.fr_index = 2
        self.feedrate = 100
        self.flowrate = [100, 100, 100]
        self.babystep = float(0)
        self.babystepx10 = 0

    def send_all(self):
        self.sendbabystep()
        self.sendfeedrate()
        self.sendflowrate()

    def sendbabystep(self):
        self.printer_if.set_babystep(self.babystep)
        # self.tempwindow.serial.send_serial("M290 Z " + str(self.babystep))

    def sendfeedrate(self):
        self.printer_if.set_feed_rate(self.feedrate)

    def sendflowrate(self):
        new_rate = self.flowrate[self.fr_index]
        if self.fr_index == 2:      # ALL extruders

            # When changing the ALL flowrate, override the individual
            # flow rates of the extruders.
            self.flowrate[0] = self.flowrate[1] = self.flowrate[2] = new_rate
            self.printer_if.set_flow_rate(new_rate)

        else:
            # Choose the string describing the extruder
            if self.fr_index == 0:  # Extruder 0
                t = "T0"
            else:                   # Extruder 1
                t = "T1"

            # Set the flow rate. Pass in the extruder string to
            # specify that the new rate applies to only one extruder.
            self.printer_if.set_flow_rate(new_rate, t)
