from qt.temperaturewindow import *
from notactiveprint_wid import *
from activeprint_wid import *
from PyQt5.QtCore import Qt
from event_hand import *

mats = ['m1', 'm2', 'm3']
periphs = ['e1', 'e2', 'bed', 'all']

class TemperatureWindow(QtWidgets.QWidget, Ui_TemperatureWindow):
	def __init__(self, serial, event_handler, parent = None):
		super(TemperatureWindow, self).__init__()
		self.setupUi(self)
		
		# if parent.fullscreen: self.fullscreen = True
		# else: self.fullscreen = False
		# if self.fullscreen: 
		# 	self.setWindowState(self.windowState() | Qt.WindowFullScreen)

		self.serial = serial
		self.parent = parent
		self.event_handler = event_handler

		self.ActivePrintWid = ActivePrintWidget(self)
		self.NotActivePrintWid = NotActivePrintWidget(self)
		self.gridLayout.addWidget(self.NotActivePrintWid, 2, 0, 1, 1)
		self.gridLayout.addWidget(self.ActivePrintWid,2,0,1,1)
		self.notactiveprint()
		self.serial.data.updateprogress.connect(self.updateprogress)
		self.serial.data.updateposition.connect(self.updateposition)

		#self.event_handler.updatetemperatures.connect(self.updatetemperatures)
		self.inittextformat(self.e1temp)
		self.inittextformat(self.e2temp)
		self.inittextformat(self.bedtemp)
		self.inittextformat(self.e1set)
		self.inittextformat(self.e2set)
		self.inittextformat(self.bedset)
		self.changeText(self.e1set, '0')
		self.changeText(self.e2set, '0')
		self.changeText(self.bedset, '0')

		self.setbuttonstyle(self.e1img)
		self.setbuttonstyle(self.e2img)
		self.setbuttonstyle(self.bedimg)

		self.initposnegbuttons()

#		Dynamic Icons
		self.fanon = False
		self.fanofficon = QtGui.QIcon()
		self.fanofficon.addPixmap(QtGui.QPixmap("img/fanoff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.fanonicon = QtGui.QIcon()
		self.fanonicon.addPixmap(QtGui.QPixmap("img/fanon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		
		self.unheated = QtGui.QIcon()
		self.bedheated1 = QtGui.QIcon()
		self.bedheated2 = QtGui.QIcon()
		self.unheated.addPixmap(QtGui.QPixmap("img/bed_unheated.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.bedheated1.addPixmap(QtGui.QPixmap("img/bed_heated1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.bedheated2.addPixmap(QtGui.QPixmap("img/bed_heated2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)


#		Initilization for Not-Printing Widget.

		self.initpreheatbuttons()
		self.NotActivePrintWid.Back.clicked.connect(self.close)
		self.NotActivePrintWid.CoolDown.clicked.connect(self.cool)
		self.NotActivePrintWid.Fan.clicked.connect(self.fan)


#		Initilization for Printing Widget.

		self.ActivePrintWid.Back.clicked.connect(self.close)
		self.ActivePrintWid.Fan.clicked.connect(self.fan)
		self.ActivePrintWid.ResumePrint.setEnabled(False)
		# self.ActivePrintWid.StopPrint.clicked.connect(self.stopprint)
		self.ActivePrintWid.PausePrint.clicked.connect(self.pauseprint)
		self.ActivePrintWid.ResumePrint.clicked.connect(self.resumeprint)
		self.ActivePrintWid.FlowrateLabel.clicked.connect(self.flowratelabel)
		self.ActivePrintWid.FlowratePos.clicked.connect(self.flowratepos)
		self.ActivePrintWid.FlowrateNeg.clicked.connect(self.flowrateneg)
		self.ActivePrintWid.BabysteppingNeg.clicked.connect(self.babystepneg)
		self.ActivePrintWid.BabysteppingPos.clicked.connect(self.babysteppos)
		self.ActivePrintWid.FeedrateSlider.valueChanged.connect(self.feedrateslider)
		self.ActivePrintWid.FeedrateSlider.sliderReleased.connect(self.sendfeedrate)

		# self.ActivePrintWid.FlowrateLabel.
		self.inittextformat(self.ActivePrintWid.FileName)
		self.inittextformat(self.ActivePrintWid.FlowrateVal)
		self.inittextformat(self.ActivePrintWid.FeedrateVal)
		self.inittextformat(self.ActivePrintWid.BabysteppingVal)
		self.inittextformat(self.ActivePrintWid.PositionLabel)
		self.setbuttonstyle(self.ActivePrintWid.FileLabel)
		self.setbuttonstyle(self.ActivePrintWid.FeedrateLabel)
		self.setbuttonstyle(self.ActivePrintWid.BabysteppingLabel)


	def update_parameters(self):
		self.event_handler.resetparameters()
		self.changeText(self.ActivePrintWid.FileName, str(self.serial.data.currentfile))
		self.changeText(self.ActivePrintWid.FeedrateVal, str(self.event_handler.feedrate))
		self.changeText(self.ActivePrintWid.BabysteppingVal, str(self.event_handler.babystep))
		self.changeText(self.ActivePrintWid.FlowrateVal, str(self.event_handler.flowrate[self.event_handler.fr_index]))

	def sendfeedrate(self):
		self.serial.send_serial("M220 S" + str(self.ActivePrintWid.FeedrateSlider.value()))

	def feedrateslider(self):
		val = self.ActivePrintWid.FeedrateSlider.value()
		self.changeText(self.ActivePrintWid.FeedrateVal, str(val))

	def babystepneg(self):
		self.event_handler.babystep -= self.event_handler.babystepinc
		self.changeText(self.ActivePrintWid.BabysteppingVal, str(self.event_handler.babystep))
		self.event_handler.sendbabystep()
	def babysteppos(self):
		self.event_handler.babystep += self.event_handler.babystepinc
		self.changeText(self.ActivePrintWid.BabysteppingVal, str(self.event_handler.babystep))
		self.event_handler.sendbabystep()

	def updateposition(self):
		pos = self.serial.data.position
		tmp = "X: "+str(pos["X"])+ " Y: "+str(pos["Y"])+ " Z: "+str(pos["Z"])+ " E: "+str(pos["E"])
		self.changeText(self.ActivePrintWid.PositionLabel, tmp)


	def updateprogress(self):
		prog = ( float(self.serial.data.progress[0])/float(self.serial.data.progress[1]) ) * 100
		self.ActivePrintWid.FileProgress.setValue(prog)

	def updateflowlabel(self):
		flow_button_text = "Flowrate: " + self.event_handler.fr_text[self.event_handler.fr_index]
		self.ActivePrintWid.FlowrateLabel.setText(flow_button_text)
		self.changeText(self.ActivePrintWid.FlowrateVal, str(self.event_handler.flowrate[self.event_handler.fr_index]))

	def flowratelabel(self):
		if self.event_handler.fr_index < 2: self.event_handler.fr_index+=1
		elif self.event_handler.fr_index == 2: self.event_handler.fr_index = 0
		self.updateflowlabel()

	def flowratepos(self):
		self.event_handler.flowrate[self.event_handler.fr_index] += 1
		self.event_handler.sendflowrate()
		self.updateflowlabel()
	def flowrateneg(self):
		self.event_handler.flowrate[self.event_handler.fr_index] -= 1
		self.event_handler.sendflowrate()
		self.updateflowlabel()


	def activeprint(self):
		self.NotActivePrintWid.hide()
		self.ActivePrintWid.show()
	def pauseprint(self):
		self.serial.send_serial("M25")
		self.ActivePrintWid.ResumePrint.setEnabled(True)
		self.ActivePrintWid.PausePrint.setEnabled(False)
		self.parent.Control.setEnabled(True)
	def resumeprint(self):
		self.serial.send_serial("M24")
		self.ActivePrintWid.ResumePrint.setEnabled(False)
		self.ActivePrintWid.PausePrint.setEnabled(True)
		self.parent.Control.setEnabled(False)

	def notactiveprint(self):
		self.NotActivePrintWid.show()
		self.ActivePrintWid.hide()

	# def stopprint(self):
	# 	self.serial.reset()
	# 	self.parent.print_pop.cancelled()
	# 	self.serial.data.resetsettemps()

	def initposnegbuttons(self):
		for p in periphs:
			if p == "all": continue
			getattr(self, p+ "pos").clicked.connect(getattr(self.event_handler, "increment_"+p))
			getattr(self, p+ "neg").clicked.connect(getattr(self.event_handler, "decrement_"+p))

	def initpreheatbuttons(self):
		for m in mats:
			for p in periphs:
				getattr(self.NotActivePrintWid, m+p).clicked.connect(getattr(getattr(self.event_handler, m), p +'set'))

	def fan(self):
		if self.serial.is_open:
			if self.fanon:
				self.serial.send_serial('M106 S0')
				self.ActivePrintWid.Fan.setIcon(self.fanofficon)
				self.ActivePrintWid.Fan.setIconSize(QtCore.QSize(65, 65))
				self.NotActivePrintWid.Fan.setIcon(self.fanofficon)
				self.NotActivePrintWid.Fan.setIconSize(QtCore.QSize(65, 65))
				self.fanon = False
			elif not self.fanon:
				self.serial.send_serial('M106 S255')
				self.ActivePrintWid.Fan.setIcon(self.fanonicon)
				self.ActivePrintWid.Fan.setIconSize(QtCore.QSize(65, 65))
				self.NotActivePrintWid.Fan.setIcon(self.fanonicon)
				self.NotActivePrintWid.Fan.setIconSize(QtCore.QSize(65, 65))
				self.fanon = True

	def cool(self):
		self.event_handler.sete1(0)
		self.event_handler.sete2(0)
		self.event_handler.setb(0)
	
	# def checkserial(self):
	# 	print self.data.serial_err
	# 	if "Disconnected" in self.serial.data.serial_err:
	# 		self.cool()
	# 		self.changeText(self.e1temp, "-----")
	# 		self.changeText(self.e2temp, "-----")
	# 		self.changeText(self.bedtemp, "-----")


	def updatetemperatures(self):
		if self.serial.is_open:
			self.changeText(self.e1temp, str(int(self.serial.data.temp["T0"][0])))
			self.changeText(self.e2temp, str(int(self.serial.data.temp["T1"][0])))
			self.changeText(self.bedtemp, str(int(self.serial.data.temp["B"][0])))
		else:
			self.changeText(self.e1temp, "-----")
			self.changeText(self.e2temp, "-----")
			self.changeText(self.bedtemp, "-----")
			self.changeText(self.e1set, "-----")
			self.changeText(self.e2set, "-----")
			self.changeText(self.bedset, "-----")
			self.event_handler.sete1temp = 0
			self.event_handler.sete2temp = 0
			self.event_handler.setbedtemp = 0
			self.serial.data.resettemps()

	def updatesettemperatures(self):
		if self.serial.is_open:
			self.changeText(self.e1set, str(int(self.serial.data.temp["T0"][1])))
			self.changeText(self.e2set, str(int(self.serial.data.temp["T1"][1])))
			self.changeText(self.bedset, str(int(self.serial.data.temp["B"][1])))
			self.event_handler.sete1temp = int(self.serial.data.temp["T0"][1])
			self.event_handler.sete2temp = int(self.serial.data.temp["T1"][1])
			self.event_handler.setbedtemp = int(self.serial.data.temp["B"][1])



	def changeText(self, label, text):
		tmp = QtWidgets.QApplication.translate("TemperatureWindow",label.format[0]+text+label.format[1],None,-1)
		label.setText(tmp)
	def inittextformat(self,label):
		label.format = label.text()
		label.format = label.format.encode("utf-8").split("-----")
	def setbuttonstyle(self,obj):
		obj.setStyleSheet("QPushButton{background: rgba(255,255,255,0); outline: none; border: none;}")

