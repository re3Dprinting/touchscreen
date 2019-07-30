from PySide2 import QtCore, QtGui, QtWidgets
from qt.module_gigabot import *



#   Gigabot Modules Class
#   Initalize gigabotmodule
class ModuleGigabot(QtWidgets.QWidget , Ui_GigabotModule):
    def __init__(self, gigabot):
        super(ModuleGigabot,self).__init__()
        self.setupUi(self)
        self.gigabot = gigabot
        self.GigabotNum.setText(gigabot.idnum)
        #self.Nozzle1Img.setScaledContents(False)
        self.Nozzle1Img.setPixmap(QtGui.QPixmap("img/nozzle1.png"))
        self.Nozzle2Img.setPixmap(QtGui.QPixmap("img/nozzle2.png"))
        self.BedImg.setPixmap(QtGui.QPixmap("img/bed_unheated.png"))
        self.StatusImg.setPixmap(QtGui.QPixmap("img/idle.png"))
        self.Nozzle1Img.setpixx()
        self.Nozzle2Img.setpixx()
        self.BedImg.setpixx()
        self.StatusImg.setpixx()

        self.updatetemps()

    def updateall(self):
        self.ModelType.setText(str(self.gigabot.model))
        self.StatusText.setText(str(self.gigabot.getstatus()))
        self.CurrentFile.setText(str(self.gigabot.currentfile))
    def updatetemps(self):
        self.Nozzle1Text.setText(str(self.gigabot.temp1))
        self.Nozzle2Text.setText(str(self.gigabot.temp2))
        self.BedText.setText(str(self.gigabot.btemp))
        QtWidgets.QApplication.processEvents()
