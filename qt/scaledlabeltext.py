from PySide2 import QtCore, QtGui, QtWidgets

class ScaledLabelText(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self)

    def inittextformat(self, parent = None):
        self.parent = parent
        self.format = self.text()
        self.format = self.format.encode("utf-8").split("-----")
        self.formatLG = self.format
#       Get the font size and calculate the smaller font for resize
        start = end = self.format[0].rfind("pt")
        start-=1
        while(self.format[0][start].isdigit()):start-=1
        smallerfont = int(self.format[0][start+1:end]) - 6
        self.formatSM = [self.format[0][:start+1] + str(smallerfont) + self.format[0][end:] , self.format[1] ]

    def changeText(self, text):
        tmp = QtWidgets.QApplication.translate("GigabotModule",self.format[0]+text+self.format[1],None,-1)
        self.setText(tmp)

    def resizeEvent(self, event):
        if self.parent.height() <220:
            self.format = self.formatSM
        elif self.parent.height() >=220:
            self.format = self.formatLG