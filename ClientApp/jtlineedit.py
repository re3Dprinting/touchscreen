from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

class JTLineEdit(QtWidgets.QLineEdit):
    focus_in = pyqtSignal()
    focus_out = pyqtSignal()

    def __init__(self, parent):
        self.super = super(JTLineEdit, self)
        self.super.__init__(parent)

    def focusInEvent(self, event):
        self.super.focusInEvent(event)
        self.focus_in.emit()

    def focusOutEvent(self, event):
        self.super.focusOutEvent(event)
        self.focus_out.emit()
