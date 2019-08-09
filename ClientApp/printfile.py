from qt.printwindow import *
from PyQt5.QtCore import Qt

class PrintWindow(QtWidgets.QWidget, Ui_PrintWindow):
	def __init__(self, serial, temp_pop, parent = None):
		super(PrintWindow, self).__init__()
		self.setupUi(self)
		self.serial = serial
		self.serial.data.updatefiles.connect(self.updatefiles)
		self.temp_pop = temp_pop
		self.parent = parent

		if parent.fullscreen: self.fullscreen = True
		else: self.fullscreen = False

		self.Back.clicked.connect(self.close)
		self.ScanSD.clicked.connect(self.scansd)
		self.StartPrint.clicked.connect(self.startprint)
		self.ActivePrint.clicked.connect(self.activeprintpop)
		self.ActivePrint.setEnabled(False)
		self.serial.data.printcancelled.connect(self.cancelled)


		self.FileList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
		self.FileList.verticalHeader().hide()
		#Stretch out the horizontal header to take up the entire view
		header = self.FileList.horizontalHeader()
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

		tabWidth = (self.tabWidget.width()/2)-24
		self.tabWidget.setStyleSheet(self.tabWidget.styleSheet() +"QTabBar::tab { width: " + str(tabWidth) + "px; }")

	def scansd(self):
		self.serial.send_serial("M22 \r")
		self.serial.send_serial("M21 \r")
		self.serial.send_serial("M20 \r")
	def updatefiles(self):
		self.FileList.setRowCount(0)
		for f in self.serial.data.files:
			rowpos = self.FileList.rowCount()

			self.FileList.insertRow(rowpos)
			file= QtWidgets.QTableWidgetItem(f)
			file.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

			size= QtWidgets.QTableWidgetItem(self.serial.data.files[f])
			size.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

			self.FileList.setItem(rowpos, 0, file)
			self.FileList.setItem(rowpos, 1, size)
	
	def cancelled(self):
		self.temp_pop.notactiveprint()

	def startprint(self):
		selected = self.FileList.currentRow()
		selected_file = self.FileList.item(selected,0)
		if selected_file != None:
			self.serial.data.currentfile = selected_file.text()
			self.serial.send_serial("M23 "+  selected_file.text())
			self.serial.send_serial("M24 \r")
			self.ActivePrint.setEnabled(True)
		self.temp_pop.activeprint()


	def activeprintpop(self):
		if self.fullscreen: self.temp_pop.showFullScreen()
		else: self.temp_pop.show()		

	def stopprint(self):
		self.serial.send_serial("M22 \r")
	#def activeprint(self):



		# else:
		# 	self.output_serial("Please select a file")