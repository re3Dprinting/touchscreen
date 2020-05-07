from builtins import str
import time
import threading
from PyQt5 import QtCore


# The Event Handler operates the temperature preheats, setting the temperatures,
#

class event_handler(QtCore.QThread):
    reconnect_serial = QtCore.pyqtSignal([str], [str])

    def __init__(self, temppage, bedcontrol):
        super(event_handler, self).__init__()
        self.temppage = temppage
        self.bedcontrol = bedcontrol
        self.bedflash = 0

    def run(self):
        while(True):
            time.sleep(0.1)
            self.flashbedicon()

    def flashbedicon(self):
        # if self.tempwindow.heatedbed.settemp >= 50:
        if self.bedcontrol.set_point >= 50:
            self.bedflash += 1
            if self.bedflash == 6:
                # self.tempwindow.bedimg.setIcon(self.tempwindow.bedheated1)
                self.temppage.bedimg.setIcon(self.temppage.bedheated1)
            elif self.bedflash == 12:
                # self.tempwindow.bedimg.setIcon(self.tempwindow.bedheated2)
                self.temppage.bedimg.setIcon(self.temppage.bedheated2)
                self.bedflash = 0
        else:
            self.temppage.bedimg.setIcon(self.temppage.unheated)
