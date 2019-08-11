from PySide2 import QtCore, QtGui, QtWidgets

#   ScaledLabelText derives from the QLabel class
class ScaledLabelText(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self)

#   The text is initialized and the font is extracted
#   Two font sizes are calculated, and upon 
    def inittextformat(self, parent = None, sizelimit = 220):
        self.parent = parent
        self.sizelimit = sizelimit
        self.format = self.text()
        self.format = self.format.encode("utf-8").split("-----")
        self.formatLG = self.format
#       Get the font size and calculate the smaller font for resize
        start = end = self.format[0].rfind("pt")
        start-=1
        while(self.format[0][start].isdigit()):start-=1
        smallerfont = int(self.format[0][start+1:end]) - 6
        self.formatSM = [self.format[0][:start+1] + str(smallerfont) + self.format[0][end:] , self.format[1] ]

#   Replacement for set text, to redefine the font size. 
    def changeText(self, text):
        tmp = QtWidgets.QApplication.translate("GigabotModule",self.format[0]+text+self.format[1],None,-1)
        self.setText(tmp)

    def currenttext(self):
        Rtf_text = self.text()
        Temp_Obj = QtWidgets.QTextEdit()
        Temp_Obj.setText(Rtf_text)
        Plain_text = Temp_Obj.toPlainText()
        del Temp_Obj
        return Plain_text

    def resizeEvent(self, event):
        # print self.parent.height()
        # #print self.formatSM
        # #print self.formatLG
        if self.parent.height() < self.sizelimit:
            self.format = self.formatSM
        elif self.parent.height() >= self.sizelimit:
            self.format = self.formatLG
        self.changeText(self.currenttext())
        #print self.text().encode("utf").remove(QRegExp("<[^>]*>"));     
        # self.parent.update_labels()
        # self.parent.update_all()