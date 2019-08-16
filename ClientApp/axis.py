

class Axis():
	def __init__(self, ax, parent = None, maxx = None, home = None):
		self.ax = ax
		self.Ax = ax.capitalize()
		self.parent = parent
		self.inc = ""
		self.gcode = ""
#		Not needed if using relative position
#		Could be implemented to prevent crashing the bed
#		But the soft limits should be on the firmware level. 
		self.maxx = maxx
		self.home = home
		self.position = float(0)

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
		# self.position += float(self.inc)
		# self.travel_limits()
		self.parent.serial.send_serial('G91')
		if self.ax == "e": self.parent.serial.send_serial('G1 '+ self.Ax+ str(self.inc) + ' F60')
		else: self.parent.serial.send_serial('G1 '+ self.Ax+ str(self.inc) + ' F4500')

	def moveneg(self):
		# self.position -= float(self.inc)
		# self.travel_limits()
		self.parent.serial.send_serial('G91')
		if self.ax == "e": self.parent.serial.send_serial('G1 '+ self.Ax+ '-'+ str(self.inc) + ' F60')
		else: self.parent.serial.send_serial('G1 '+ self.Ax+ '-'+str(self.inc) + ' F4500')