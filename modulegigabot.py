from PySide2 import QtCore, QtGui, QtWidgets
from qt.module_gigabot import *

from moreinfowindow import *
#   Gigabot Modules Class
#   Initalize gigabotmodule
class ModuleGigabot(QtWidgets.QWidget , Ui_GigabotModule):
    def __init__(self, gigabot):
        super(ModuleGigabot,self).__init__()
        self.setupUi(self)
        self.gigabot = gigabot
        self.activeflash = True
        self.bedflash = 0

        self.update_ver_num()
        #self.Nozzle1Img.setScaledContents(False)
        self.Nozzle1Img.changepix("img/nozzle1.png")
        self.Nozzle2Img.changepix("img/nozzle2.png")
        self.BedImg.changepix("img/bed_unheated.png")
        self.StatusImg.changepix("img/idle.png")
        #self.setallpix()
        self.updateall()
        self.ViewMachineInfo.clicked.connect(self.moreinfo)


    def moreinfo(self):
        self.pop = MoreInfoWindow(self.gigabot, self)
        self.pop.show()
        self.pop.update_ver_num.connect(self.update_ver_num)

    def update_ver_num(self):
        self.GigabotVersion.setText(self.gigabot.version)
        self.GigabotNum.setText(self.gigabot.idnum)

    def updateall(self):
        self.ModelType.setText(str(self.gigabot.model))
        self.StatusText.setText(str(self.gigabot.getstatus()))
        self.CurrentFile.setText(str(self.gigabot.currentfile))
        self.Nozzle1Text.setText(self.gigabot.gettemp1())
        self.Nozzle2Text.setText(self.gigabot.gettemp2())
        self.BedText.setText(self.gigabot.getbtemp())
        if self.gigabot.status == "ON":
            self.StatusImg.changepix("img/idle.png")
            self.BedImg.changepix("img/bed_unheated.png")
            self.CurrentFile.setText("~~~~~")
        elif self.gigabot.status == "AC":
            if self.activeflash: 
                self.StatusImg.changepix("img/active.png")
            else: 
                self.StatusImg.changepix("img/off.png")
            if self.bedflash == 2:
                self.BedImg.changepix("img/bed_unheated.png")
            elif self.bedflash == 4:
                self.BedImg.changepix("img/bed_heated1.png")
            elif self.bedflash == 6:
                self.BedImg.changepix("img/bed_heated2.png")
                self.bedflash = 0
            self.bedflash += 1
            self.activeflash = not self.activeflash
        elif self.gigabot.status == "OF":
            self.BedImg.changepix("img/bed_unheated.png")
            self.StatusImg.changepix("img/off.png")
            self.CurrentFile.setText("~~~~~")
            self.CurrentFile.setText("~~ / ~~")
            self.Nozzle1Text.setText("~~ / ~~")
            self.Nozzle2Text.setText("~~ / ~~")
            self.BedText.setText("~~ / ~~")

    def checkvisible(self):
        if self.gigabot.modulelinked and not self.gigabot.module.isVisible():
            self.gigabot.moduleshow = False

    # def setallpix(self):
    #     self.Nozzle1Img.setpix()
    #     self.Nozzle2Img.setpix()
    #     self.BedImg.setpix()
    #     self.StatusImg.setpix()