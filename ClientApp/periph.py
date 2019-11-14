from builtins import str
from builtins import object
import PyQt5


class Periph(object):
    def __init__(self, periph, command, maxtemp, parent):
        self.periph = periph
        self.command = command
        self.maxtemp = maxtemp
        self.parent = parent

        self.timer = PyQt5.QtCore.QTimer()
        self.timer.timeout.connect(self.button_event_check)
        self.button_held_time = 0
        self.direction = "inc"

        self.settemp = 0

        self.init_posneg()

    def init_posneg(self):
        getattr(self.parent, self.periph +
                "pos").clicked.connect(self.increment)
        getattr(self.parent, self.periph +
                "neg").clicked.connect(self.decrement)

        getattr(self.parent, self.periph +
                "pos").pressed.connect(self.incrementbuttonpressed)
        getattr(self.parent, self.periph +
                "neg").pressed.connect(self.decrementbuttonpressed)

        getattr(self.parent, self.periph +
                "pos").released.connect(self.buttonreleased)
        getattr(self.parent, self.periph +
                "neg").released.connect(self.buttonreleased)

    def incrementbuttonpressed(self):
        self.timer.start(12)
        self.direction = "inc"

    def decrementbuttonpressed(self):
        self.timer.start(12)
        self.direction = "dec"

    def buttonreleased(self):
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
            if self.direction == "inc":
                self.increment()
            elif self.direction == "dec":
                self.decrement()

    def increment(self):
        if self.settemp < self.maxtemp:
            self.settemp += 1
        self.parent.changeText(
            getattr(self.parent, self.periph + "set"), str(self.settemp))

    def decrement(self):
        if self.settemp > 0:
            self.settemp -= 1
        self.parent.changeText(
            getattr(self.parent, self.periph + "set"), str(self.settemp))

    def setandsend(self, num):
        self.set(num)
        self.sendtemp()

    def set(self, num):
        self.settemp = num
        self.parent.changeText(
            getattr(self.parent, self.periph + "set"), str(self.settemp))

    def sendtemp(self):
        self.parent.serial.send_serial(self.command + str(self.settemp))
        self.parent.serial.send_serial("M105")
        self.parent.event_handler.sendtempcount = 0
