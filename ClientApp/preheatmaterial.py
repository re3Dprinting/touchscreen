
class Material():
	def __init__(self, e1, e2, bed, parent = None):
		self.parent = parent
		self.e1 = e1
		self.e2 = e2
		self.bed = bed
	def e1set(self):
		self.parent.sete1(self.e1)
	def e2set(self):
		self.parent.sete2(self.e2)
	def bedset(self):
		self.parent.setb(self.bed)
	def allset(self):
		self.e1set()
		self.e2set()
		self.bedset()
