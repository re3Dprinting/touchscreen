from PyQt5 import QtWidgets


class BasePage(QtWidgets.QWidget):
    def __init__(self):
        super(BasePage, self).__init__()

    def _log(self, message):
        self._logger.debug(message)

        # Global function that allows windows to create a borderless button
    def setAllStyleProperty(self, listobj, prop):
        for obj in listobj:
            obj.setProperty("cssClass", prop)

    def setAllTransparentButton(self, listobj):
        self.setAllStyleProperty(listobj, "transparent_button")

    def setAllTransparentIcon(self, listobj):
        self.setAllStyleProperty(listobj, "transparent_icon")

    def setStyleProperty(self, obj, prop):
        obj.setProperty("cssClass", prop)

    def setTransparentButton(self, obj):
        self.setStyleProperty(obj, "transparent_button")

    def setTransparentIcon(self, obj):
        self.setStyleProperty(obj, "transparent_icon")

    def back(self):
        self._log("UI: User touched Back")
        self.ui_controller.pop()
