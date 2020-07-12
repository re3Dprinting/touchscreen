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

        self.popup_button.clicked.connect(self.hide)
        # self.popup_title.setText("Filament Change")
        # self.popup_message.setText("Filament purge in progress. Please wait...")

        self.setAllStyleProperty([self.popup_details, self.popup_message], "black-transparent-text font-m align-center")
        self.setAllStyleProperty([self.popup_title], "black-transparent-text font-l align-center")
        self.setAllStyleProperty([self.popup_button], "btn-font-s black-text btn-pressed-light yellow-btn")

    def _log(self, message):
        self._logger.debug(message)