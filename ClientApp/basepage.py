from PyQt5 import QtWidgets, QtCore


class BasePage(QtWidgets.QWidget):
    def __init__(self):
        super(BasePage, self).__init__()

    def _log(self, message):
        self._logger.debug(message)

        # Global function that allows windows to create a borderless button
    def setAllStyleProperty(self, listobj, prop):
        for obj in listobj:
            obj.setProperty("cssClass", prop)

    def setAllTransparentButton(self, listobj, dark=False):
        if dark:
            color = "btn-pressed-dark"
        else:
            color = "btn-pressed-light"

        for obj in listobj:
            size = min(obj.width(), obj.height())
            # print(obj.objectName(), size)

            obj.setProperty("cssClass", color + " transparent-btn")
            obj.setStyleSheet(
                "QPushButton:pressed{border-radius:"+str(int(size/2))+";}")

    def setAllTransparentIcon(self, listobj):
        self.setAllStyleProperty(listobj, "transparent-icon")

    def setStyleProperty(self, obj, prop):
        obj.setProperty("cssClass", prop)

    def setTransparentButton(self, obj):
        self.setStyleProperty(obj, "transparent-btn")

    def setTransparentIcon(self, obj):
        self.setStyleProperty(obj, "transparent-icon")

    def back(self):
        self._log("UI: User touched Back")
        self.ui_controller.pop()
