
from builtins import object
class Material(object):
	def __init__(self, e1, e2, bed, parent = None):
		self.parent = parent
		self.e1 = e1
		self.e2 = e2
		self.bed = bed
		
	def e1set(self):
		self.parent.extruder1.setandsend(self.e1)
	def e2set(self):
		self.parent.extruder2.setandsend(self.e2)
	def bedset(self):
		self.parent.heatedbed.setandsend(self.bed)
	def allset(self):
		self.e1set()
		self.e2set()
		self.bedset()
