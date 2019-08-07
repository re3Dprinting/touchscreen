

class Axis():
	def __init__(self, ax, parent = None, maxx = None, home = None):
		self.ax = ax
		self.Ax = ax.capitalize()
		self.parent = parent
		self.inc = ""
		self.position = float(0)
		self.gcode = ""
		self.maxx = maxx
		self.home = home

		self.init_movement()
		self.init_increment()

	def init_movement(self):
		self.parent
		getattr(self.parent, self.Ax + "Pos").clicked.connect(self.movepos)
		getattr(self.parent, self.Ax + "Neg").clicked.connect(self.moveneg)

	def init_increment(self):
		self.inc = getattr(self.parent, self.ax + "button").checkedButton().text()
		getattr(self.parent, self.ax + "button").buttonClicked.connect(self.updateincrement)

	def updateincrement(self):
		self.inc = getattr(self.parent, self.ax + "button").checkedButton().text()
	def travel_limits(self):
		if self.maxx != None and self.position > self.maxx: self.position = self.maxx
		if self.position < 0 and self.ax != 'e': self.position = 0
	def movepos(self):
		self.position += float(self.inc)
		self.travel_limits()
		self.parent.serial.send_serial('G0 '+ self.Ax+ str(self.position))
	def moveneg(self):
		self.position -= float(self.inc)
		self.travel_limits()
		self.parent.serial.send_serial('G0 '+ self.Ax+ str(self.position))