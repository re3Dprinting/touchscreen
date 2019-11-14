from qt.notactiveprintwidget import *
from PyQt5.QtCore import Qt


class NotActivePrintWidget(QtWidgets.QWidget, Ui_NotActivePrintWidget):
    def __init__(self, parent=None):
        super(NotActivePrintWidget, self).__init__()
        self.setupUi(self)
