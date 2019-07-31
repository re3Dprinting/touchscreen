from qt.module_moreinfo import *

class MoreInfoWindow(QtWidgets.QWidget, Ui_MoreInfoWindow):
	def __init__(self, gigabot):
		super(MoreInfoWindow, self).__init__()
		self.setupUi(self)
		self.gigabot = gigabot
