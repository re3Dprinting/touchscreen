from qt.touchdisplaywindow import *
from PySide2.QtCore import Qt
import sys

class TouchDisplay(QtWidgets.QWidget, Ui_TouchDisplay):
    def __init__(self, parent = None):
        super(TouchDisplay, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.printsomething)
    def printsomething(self):
    	self.textBrowser.append("Hello world")

if __name__ == '__main__':

	app = QtWidgets.QApplication(sys.argv)
	display = TouchDisplay()
	display.show()
	app.exec_()