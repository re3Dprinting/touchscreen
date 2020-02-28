import logging
from .basewindow import BaseWindow
from qt.infowindow import *

class InfoWindow(BaseWindow, Ui_InfoWindow):
    def __init__(self, printer_if, parent=None):
        super(InfoWindow, self).__init__(parent)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("InfoWindow __init__()")

        # Set up user interface
        self.setupUi(self)
        self.parent = parent

        # Save reference to printer interface
        self.printer_if = printer_if

        # Set up callback functions
        self.Back.clicked.connect(self.back)
