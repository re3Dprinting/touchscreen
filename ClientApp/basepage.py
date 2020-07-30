from PyQt5 import QtWidgets, QtCore
from util.log import tsLogger

class BasePage(QtWidgets.QWidget, tsLogger):
    popup_signal = QtCore.pyqtSignal(str, str, str, bool)
    def __init__(self):
        super(BasePage, self).__init__()

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
        self.ui_controller.pop()
