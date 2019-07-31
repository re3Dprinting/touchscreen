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

        self.GigabotVersion.inittextformat(self)
        self.ModelType.inittextformat(self)
        self.GigabotNum.inittextformat(self)

        self.StatusLabel.inittextformat(self)
        self.StatusText.inittextformat(self)
        self.FileLabel.inittextformat(self)
        self.FileText.inittextformat(self)

        self.Nozzle1Text.inittextformat(self)
        self.Nozzle2Text.inittextformat(self)
        self.BedText.inittextformat(self)

        self.update_labels()
        self.update_all()

        #self.Nozzle1Img.setScaledContents(False)
        self.Nozzle1Img.changepix("img/nozzle1.png")
        self.Nozzle2Img.changepix("img/nozzle2.png")
        self.BedImg.changepix("img/bed_unheated.png")
        self.StatusImg.changepix("img/idle.png")
        self.ViewMachineInfo.clicked.connect(self.moreinfo)

    def moreinfo(self):
        self.pop = MoreInfoWindow(self.gigabot, self)
        self.pop.show()
        self.pop.update_ver_num.connect(self.update_title)

    def update_title(self):
        self.GigabotVersion.changeText(self.gigabot.version)
        self.GigabotNum.changeText(self.gigabot.idnum)
#   Function called to resize all labels when the window is resized
    def update_labels(self):
        self.GigabotVersion.changeText(self.gigabot.version)
        self.GigabotNum.changeText(self.gigabot.idnum)
        self.ModelType.changeText(self.gigabot.model) 
        self.StatusLabel.changeText("Status:")
        self.FileLabel.changeText("File:")
    def update_all(self):
        self.ModelType.changeText(str(self.gigabot.model))
        self.StatusText.changeText(str(self.gigabot.getstatus()))
        self.FileText.changeText(str(self.gigabot.currentfile))
        self.Nozzle1Text.changeText(self.gigabot.gettemp1())
        self.Nozzle2Text.changeText(self.gigabot.gettemp2())
        self.BedText.changeText(self.gigabot.getbtemp())
        if self.gigabot.status == "ON":
            self.StatusImg.changepix("img/idle.png")
            self.BedImg.changepix("img/bed_unheated.png")
            self.FileText.changeText("~~~~~")
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
            self.FileText.changeText("~~~~~")
            self.Nozzle1Text.changeText("~~ / ~~")
            self.Nozzle2Text.changeText("~~ / ~~")
            self.BedText.changeText("~~ / ~~")
    def resizeEvent(self, event):
        self.update_labels()
        self.update_all()

    def checkvisible(self):
        if self.gigabot.widgetlinked and not self.gigabot.widget.isVisible():
            self.gigabot.widgetshow = False

    # def setallpix(self):
    #     self.Nozzle1Img.setpix()
    #     self.Nozzle2Img.setpix()
    #     self.BedImg.setpix()
    #     self.StatusImg.setpix()
