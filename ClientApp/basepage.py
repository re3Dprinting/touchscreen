from PyQt5 import QtWidgets

class BasePage(QtWidgets.QWidget):
    def __init__(self):
        super(BasePage, self).__init__()

    def _log(self, message):
        self._logger.debug(message)

    def setbuttonstyle(self, obj):
        obj.setStyleSheet(
            "QPushButton { background: rgba(255,255,255,0); outline: none; border: none; } QPushButton:checked{background: rgba(255,255,255,0); outline: none; border: none;} QPushButton:pressed { background: rgba(0,0,0,0.1); outline: none; border: none; }")

    def back(self):
        self._log("UI: User touched Back")
        self.ui_controller.pop()
