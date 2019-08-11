from PySide2 import QtCore
from qt.module_moreinfo import *
from PySide2.QtCore import Qt

class MoreInfoWindow(QtWidgets.QWidget, Ui_MoreInfoWindow):
	update_ver_num = QtCore.Signal([str],[unicode])
	def __init__(self, gigabot, parent = None):
		super(MoreInfoWindow, self).__init__()
		self.setupUi(self)
		self.gigabot = gigabot
		self.DataOutput.setText(gigabot.getstats())
		self.VersionInput.setText(gigabot.version)
		self.NumberInput.setText(gigabot.idnum)
#       Move Window to Middle of Screen
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		self.setWindowFlags(Qt.Tool)

		ok = self.Button.button(QtWidgets.QDialogButtonBox.Ok)
		ok.clicked.connect(self.okayclick)

	def okayclick(self):
		self.gigabot.version = self.VersionInput.toPlainText()
		self.gigabot.idnum = self.NumberInput.toPlainText()
		self.update_ver_num.emit("update_ver_num")
		self.close()
