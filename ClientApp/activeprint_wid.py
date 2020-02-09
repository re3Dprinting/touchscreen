from .qt.activeprintwidget import *
from PyQt5.QtCore import Qt


class ActivePrintWidget(QtWidgets.QWidget, Ui_ActivePrintWidget):
    def __init__(self, parent=None):
        super(ActivePrintWidget, self).__init__()
        self.setupUi(self)
