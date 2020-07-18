import logging
from PyQt5.QtCore import Qt, pyqtSignal
from .qt.popup import *
from basepage import BasePage

class PopUp(QtWidgets.QDialog, BasePage, Ui_PopUpWindow):
    # runout_signal = pyqtSignal(str, str)

    def __init__(self, parent):
        super(PopUp, self).__init__()
        self._logger = logging.getLogger(__name__)
        self._log("PopUp Window Appeared")

        self.parent = parent

        self.setupUi(self)
        self.setModal(True)
        # self.setAttribute(Qt.WA_NoSystemBackground)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setAutoFillBackground(False)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowFlags(self.windowFlags() |  QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)



        self.popup_button.clicked.connect(self.hide)
        # self.popup_title.setText("Filament Change")
        # self.popup_message.setText("Filament purge in progress. Please wait...")

        self.setAllStyleProperty([self.popup_details, self.popup_message], "black-transparent-text font-m align-center")
        self.setAllStyleProperty([self.popup_title], "black-transparent-text font-l align-center")
        self.setAllStyleProperty([self.popup_button], "btn-font-s black-text btn-pressed-light yellow-btn")
        self.setAllStyleProperty([self.PopUpMain], "pop-up")
        self.setAllStyleProperty([self], "transparent")

    def _log(self, message):
        self._logger.debug(message)
