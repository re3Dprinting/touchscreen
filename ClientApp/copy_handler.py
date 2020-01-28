from PyQt5.QtCore import Qt, pyqtSignal
from .qt.copy_dialog import *

class  CopyHandlerDialog(QtWidgets.QWidget, Ui_WCopyDialog):
    runout_signal = pyqtSignal(str, str)

    def __init__(self, parent):
        super(CopyHandlerDialog, self).__init__()
        self.setupUi(self)

    def accept(self):
        pass

    def reject(self):
        pass
