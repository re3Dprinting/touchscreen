from qt.touchdisplaywindow import *
from PyQt5.QtCore import Qt
import sys

class TouchDisplay(QtWidgets.QWidget, Ui_TouchDisplay):
    def __init__(self, parent = None):
        super(TouchDisplay, self).__init__()
        self.setupUi(self)
        #self.showFullScreen()
        self.Control.setCheckable(False)
        self.Control.setStyleSheet("QPushButton{background: transparent; outline: none;}")
        
        self.Print.setStyleSheet("QPushButton{background: transparent; outline: none;}");
        self.Settings.setStyleSheet("QPushButton{background: transparent; outline: none;}");
        #self.pushButton.clicked.connect(self.printsomething)

if __name__ == '__main__':

	app = QtWidgets.QApplication(sys.argv)
	display = TouchDisplay()
	display.show()
	app.exec_()
