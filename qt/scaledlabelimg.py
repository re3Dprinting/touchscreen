from PySide2 import QtCore, QtGui, QtWidgets

#   ScaleLabelImg class derives from QLabel
#   Used to maintain the aspect ratio when the main window on the dashboard is resized. 
class ScaledLabelImg(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self)

#   set the _pixmap value, whenever the file is changed.         
    def setpix(self):
        self._pixmap = QtGui.QPixmap(self.pixmap())
#   upon resizing, scale the image while maintaining the aspect ratio
    def resizeEvent(self, event):
        self.setPixmap(self._pixmap.scaled(self.width(), self.height(),QtCore.Qt.KeepAspectRatio))
#   changepix function replaces setPixmap. 
#   sets the new pixmap, redefines the _pixmap value, then resizes. 
    def changepix(self, file):
        self.setPixmap(QtGui.QPixmap(file))
        self.setpix()
        self.resizeEvent(self)