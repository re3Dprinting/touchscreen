from builtins import object
import logging
from util.log import tsLogger

class Material(tsLogger):
    def __init__(self, name, \
                 e0_control, e1_control, bed_control, \
                 e0_temp, e1_temp, bed_temp):

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log_d("Material __init__ <%s>/%d/%d/%d" % (name, e0_temp, e1_temp, bed_temp))

        self.name = name
        self.e0_control = e0_control
        self.e1_control = e1_control
        self.bed_control = bed_control
        self.e0_temp = e0_temp
        self.e1_temp = e1_temp
        self.bed_temp = bed_temp

    def e0set(self):
        self._log_d("UI: User touched <%s> extruder 0 preset (%d)." % (self.name, self.e0_temp))
        self.e0_control.set_setpoint(self.e0_temp)

    def e1set(self):
        self._log_d("UI: User touched <%s> extruder 1 preset (%d)." % (self.name, self.e1_temp))
        self.e1_control.set_setpoint(self.e1_temp)

    def bedset(self):
        self._log_d("UI: User touched <%s> bed preset (%d)." % (self.name, self.bed_temp))
        self.bed_control.set_setpoint(self.bed_temp)

    def allset(self):
        self._log_d("UI: User touched <%s> ALL preset (%d/%d/%d)."
                  % (self.name, self.e0_temp, self.e1_temp, self.bed_temp))
        self.e0_control.set_setpoint(self.e0_temp)
        self.e1_control.set_setpoint(self.e1_temp)
        self.bed_control.set_setpoint(self.bed_temp)
