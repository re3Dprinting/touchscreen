from PyQt5 import QtWidgets


class BasePage(QtWidgets.QWidget):
    def __init__(self):
        super(BasePage, self).__init__()

    def _log(self, message):
        self._logger.debug(message)

        # Global function that allows windows to create a borderless button
    def setTransparentButton(self, obj):
        obj.setProperty("cssClass", "transparent_button")

    def setTransparentIcon(self, obj):
        obj.setProperty("cssClass", "transparent_icon")

    def back(self):
        self._log("UI: User touched Back")
        self.ui_controller.pop()
