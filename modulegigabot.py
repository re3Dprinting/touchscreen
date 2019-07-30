from PySide2 import QtCore, QtGui, QtWidgets
from qt.module_gigabot import *



#   Gigabot Modules Class
#   Initalize gigabotmodule
class ModuleGigabot(QtWidgets.QWidget , Ui_GigabotModule):
    def __init__(self, gigabot):
        super(ModuleGigabot,self).__init__()
        self.setupUi(self)
        self.gigabot = gigabot
        self.activeflash = True

        self.GigabotNum.setText(gigabot.idnum)
        #self.Nozzle1Img.setScaledContents(False)
        self.Nozzle1Img.changepix("img/nozzle1.png")
        self.Nozzle2Img.changepix("img/nozzle2.png")
        self.BedImg.changepix("img/bed_unheated.png")
        self.StatusImg.changepix("img/idle.png")
        self.updateall()


    def updateall(self):
        self.ModelType.setText(str(self.gigabot.model))
        self.StatusText.setText(str(self.gigabot.getstatus()))
        self.CurrentFile.setText(str(self.gigabot.currentfile))
        self.Nozzle1Text.setText(str(self.gigabot.temp1))
        self.Nozzle2Text.setText(str(self.gigabot.temp2))
        self.BedText.setText(str(self.gigabot.btemp))
        if self.gigabot.status == "ON":
            self.StatusImg.changepix("img/idle.png")
            self.CurrentFile.setText("~~~~~")
        elif self.gigabot.status == "AC":
            if self.activeflash: 
                self.StatusImg.changepix("img/active.png")
            else: 
                self.StatusImg.changepix("img/off.png")
            self.activeflash = not self.activeflash
        elif self.gigabot.status == "OF":
            self.StatusImg.changepix("img/off.png")
            self.CurrentFile.setText("~~~~~")
     


    def checkvisible(self):
        self.checkvisibility()

    def setallpix(self):
        self.Nozzle1Img.setpix()
        self.Nozzle2Img.setpix()
        self.BedImg.setpix()
        self.StatusImg.setpix()

    def checkvisibility(self):
        if self.gigabot.modulelinked and not self.gigabot.module.isVisible():
            self.gigabot.moduleshow = False