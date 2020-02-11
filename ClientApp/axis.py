from builtins import str
from builtins import object
import logging
import PyQt5


class Axis(object):
    def __init__(self, ax, feedrate, parent=None, holdmove=None):
        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("Axis __init__()")

        self.feedrate = feedrate
        self.ax = ax
        self.Ax = ax.capitalize()
        self.parent = parent
        self.holdmove = holdmove

        self.timer = PyQt5.QtCore.QTimer()
        self.timer.timeout.connect(self.button_event_check)
        self.button_held_time = 0
        self.held_count = 0
        self.direction = "Pos"

        self.inc = ""
        self.gcode = ""
#	Not needed if using relative position
#	Could be implemented to prevent crashing the bed
#	But the soft limits should be on the firmware level.
        self.position = float(0)

        self.init_movement()
        self.init_increment()

    def _log(self, message):
        self._logger.debug(message)

    def init_movement(self):

        #getattr(self.parent, self.Ax + "Pos").clicked.connect(self.movepos)
        getattr(self.parent, self.Ax + "Pos").pressed.connect(self.posbuttonpressed)
        getattr(self.parent, self.Ax + "Pos").released.connect(self.buttonreleased)

        #getattr(self.parent, self.Ax + "Neg").clicked.connect(self.moveneg)
        getattr(self.parent, self.Ax + "Neg").pressed.connect(self.negbuttonpressed)
        getattr(self.parent, self.Ax + "Neg").released.connect(self.buttonreleased)

    def posbuttonpressed(self):
        self._log("UI: User touched <%s> +" % self.Ax)
        self.held_count = 0
        self.timer.start(250)
        self.direction = "Pos"

    def negbuttonpressed(self):
        self._log("UI: User touched <%s> -" % self.Ax)
        self.held_count = 0
        self.timer.start(250)
        self.direction = "Neg"

    def buttonreleased(self):
        if self.held_count > 0:
            self._log("UI: User released button after %d counts." % self.held_count)
        self.timer.stop()
        if (self.button_held_time == 0 or self.holdmove == None) and self.direction == "Pos":
            self.movepos()
        elif (self.button_held_time == 0 or self.holdmove == None) and self.direction == "Neg":
            self.moveneg()
        self.button_held_time = 0

    def button_event_check(self):
        self.button_held_time += 0.25
        if self.holdmove != None:
            self.held_count += 1
            if self.direction == "Pos":
                self.movepos(self.holdmove)
            elif self.direction == "Neg":
                self.moveneg(self.holdmove)

    def init_increment(self):
        self.inc = getattr(self.parent, self.ax +
                           "button").checkedButton().text()
        self._log("UI: Increment = %s" % self.inc)
        getattr(self.parent, self.ax +
                "button").buttonClicked.connect(self.updateincrement)

    def updateincrement(self):
        self.inc = getattr(self.parent, self.ax +
                           "button").checkedButton().text()
        self._log("UI: User set <%s> increment to <%s>" % (self.ax, self.inc))

    def travel_limits(self):
        if self.maxx != None and self.position > self.maxx:
            self.position = self.maxx
        if self.position < 0 and self.ax != 'e':
            self.position = 0

    def movepos(self, inc=None):
        if inc == None:
            inc = self.inc
        # self.parent.serial.send_serial('G91')
        self.parent.printer_if.relative_positioning();
        movement_command = 'G1 ' + self.Ax + str(inc) + ' F' + self.feedrate
        # print("Sending <%s>" % (movement_command))
        self.parent.printer_if.commands(movement_command)

        # self.parent.serial.send_serial(
        #     'G1 ' + self.Ax + str(inc) + ' F' + self.feedrate)

    def moveneg(self, inc=None):
        if inc == None:
            inc = self.inc
        self.parent.printer_if.relative_positioning();
        movement_command = 'G1 ' + self.Ax + "-" + str(inc) + ' F' + self.feedrate
        # print("Sending <%s>" % (movement_command))
        self.parent.printer_if.commands(movement_command)

        # self.parent.serial.send_serial('G91')
        # self.parent.serial.send_serial(
        #     'G1 ' + self.Ax + '-' + str(inc) + ' F' + self.feedrate)
