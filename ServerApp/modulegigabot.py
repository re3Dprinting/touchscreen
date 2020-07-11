from PySide2 import QtCore, QtGui, QtWidgets
from qt.module_gigabot import *

from moreinfowindow import *

#   Gigabotmodule class derived from the generated ui class, Ui_GigabotModule


class ModuleGigabot(QtWidgets.QWidget, Ui_GigabotModule):
    def __init__(self, gigabot):
        super(ModuleGigabot, self).__init__()
        self.setupUi(self)
        self.resize(430, 280)
        self.gigabot = gigabot
        self.activeflash = True
        self.bedflash = 0

#       Initialize the resizable labels.
        self.init_labels()

#       Set up the initial text for the labels.
        self.update_labels()
        self.update_all()

#       Set the pixmap of the labels
        self.setTransparentButton(self.Nozzle1Img)
        self.setTransparentButton(self.Nozzle2Img)
        self.setTransparentButton(self.BedImg)
        self.changeicon(self.Nozzle1Img, "img/nozzle1.png")
        self.changeicon(self.Nozzle2Img, "img/nozzle1.png")
        self.changeicon(self.BedImg, "img/bed_unheated.png")
        #self.changeicon(self.StatusImg, "img/idle.png")
        # self.Nozzle1Img.changepix("img/nozzle1.png")
        # self.Nozzle2Img.changepix("img/nozzle1.png")
        # self.BedImg.changepix("img/bed_unheated.png")
        self.StatusImg.changepix("img/idle.png")

#       Connect the machineinfo button to the appropriate function
        self.ViewMachineInfo.clicked.connect(self.moreinfo)

        self.unheated = QtGui.QIcon()
        self.bedheated1 = QtGui.QIcon()
        self.unheated.addPixmap(QtGui.QPixmap(
            "img/bed_unheated.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bedheated1.addPixmap(QtGui.QPixmap(
            "img/bed_heated1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

#   More info screen pops up then updates the title
    def moreinfo(self):
        self.pop = MoreInfoWindow(self.gigabot, self)
        self.pop.show()
        self.pop.update_ver_num.connect(self.update_title)

    def init_labels(self):
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
        self.SetNozzle1Text.inittextformat(self)
        self.SetNozzle2Text.inittextformat(self)
        self.SetBedText.inittextformat(self)

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

#   Update_all is called periodically to update the module with
#   new gigabot object data.
    def update_all(self):
        self.ModelType.changeText(str(self.gigabot.model))
        self.StatusText.changeText(str(self.gigabot.getstatus()))
        self.FileText.changeText(str(self.gigabot.currentfile))

        self.Nozzle1Text.changeText(self.gigabot.gettemp1())
        self.Nozzle2Text.changeText(self.gigabot.gettemp2())
        self.BedText.changeText(self.gigabot.getbtemp())

        self.SetNozzle1Text.changeText(self.gigabot.getsettemp1())
        self.SetNozzle2Text.changeText(self.gigabot.getsettemp2())
        self.SetBedText.changeText(self.gigabot.getsetbtemp())

        if self.gigabot.status == "ON":
            self.StatusImg.changepix("img/idle.png")
            # self.BedImg.changepix("img/bed_unheated.png")
            self.changeicon(self.BedImg, "img/bed_unheated.png")
            self.FileText.changeText("~~~~~")
        elif self.gigabot.status == "AC":
            if self.activeflash:
                self.StatusImg.changepix("img/active.png")
                # self.Nozzle1Img.changepix("img/nozzle1.png")
                # self.Nozzle2Img.changepix("img/nozzle1.png")
                self.changeicon(self.Nozzle1Img, "img/nozzle1.png")
                self.changeicon(self.Nozzle2Img, "img/nozzle1.png")
            else:
                self.StatusImg.changepix("img/off.png")
                # self.Nozzle1Img.changepix("img/nozzle2.png")
                # self.Nozzle2Img.changepix("img/nozzle2.png")
                self.changeicon(self.Nozzle1Img, "img/nozzle2.png")
                self.changeicon(self.Nozzle2Img, "img/nozzle2.png")
            if self.bedflash == 2:
                # self.BedImg.changepix("img/bed_unheated.png")
                self.changeicon(self.BedImg, "img/bed_unheated.png")
            elif self.bedflash == 4:
                # self.BedImg.changepix("img/bed_heated1.png")
                self.changeicon(self.BedImg, "img/bed_heated1.png")
            elif self.bedflash == 6:
                # self.BedImg.changepix("img/bed_heated2.png")
                self.changeicon(self.BedImg, "img/bed_heated2.png")
                self.bedflash = 0
            self.bedflash += 1
            self.activeflash = not self.activeflash
        elif self.gigabot.status == "OF":
            # self.BedImg.changepix("img/bed_unheated.png")
            self.StatusImg.changepix("img/off.png")
            self.changeicon(self.BedImg, "img/bed_unheated.png")
            self.FileText.changeText("~~~~~")
            self.Nozzle1Text.changeText("~~")
            self.Nozzle2Text.changeText("~~")
            self.BedText.changeText("~~")
            self.SetNozzle1Text.changeText("~~")
            self.SetNozzle2Text.changeText("~~")
            self.SetBedText.changeText("~~")

    def setTransparentButton(self, obj):
        obj.setStyleSheet(
            "QPushButton{background: rgba(255,255,255,0); outline: none; border: none;}")

    def changeicon(self, obj, icon):
        newicon = QtGui.QIcon()
        #newicon.setIconSize(QtCore.QSize(55, 55))
        newicon.addPixmap(QtGui.QPixmap(
            icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        obj.setIcon(newicon)
    # Upon resize, update the labels and all of the text.
    # def resizeEvent(self, event):
    #     self.update_labels()
    #     self.update_all()
