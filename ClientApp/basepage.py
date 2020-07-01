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

    def setAllTransparentButton(self, listobj, dark=False):
        if dark:
            color = "btn-pressed-dark"
        else:
            color = "btn-pressed-light"

        for obj in listobj:
            size = min(obj.width(), obj.height())
            # print(obj.objectName(), size)
            if size <= 50:
                obj.setProperty(
                    "cssClass", "btn-pressed-s " + color + " transparent-btn")
            elif size > 50 and size <= 75:
                obj.setProperty(
                    "cssClass", "btn-pressed-m " + color + " transparent-btn")
            elif size > 75 and size <= 100:
                obj.setProperty(
                    "cssClass", "btn-pressed-l " + color + " transparent-btn")
            elif size > 100:
                obj.setProperty(
                    "cssClass", "btn-pressed-xl " + color + " transparent-btn")

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
