from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from qt.addlabelwindow import *
from qt.scaledlabeltext import *

class AddLabel(QtWidgets.QWidget, Ui_addlabel):
	def __init__(self, parent = None):
		super(AddLabel, self).__init__()
		self.setupUi(self)
		self.parent = parent
		self.setWindowFlags(Qt.Tool)
#		Move Window to Middle of Screen
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

		close = self.Button.button(QtWidgets.QDialogButtonBox.Cancel)
		close.clicked.connect(self.close)
		ok = self.Button.button(QtWidgets.QDialogButtonBox.Ok)
		ok.clicked.connect(self.addlabel)

	def addlabel(self):
		wid = QtWidgets.QDockWidget(self.parent)
		addedlabel = ScaledLabelText(wid)
		addedlabel.setText(QtWidgets.QApplication.translate("widget", "<html><head/><body><p align=\"center\"><span style=\" font-size:30pt;\">-----</span></p></body></html>", None, -1))
		addedlabel.inittextformat(wid, 70)
		addedlabel.changeText(self.LabelInput.toPlainText())
		wid.setWidget(addedlabel)
		wid.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
		wid.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable)
		wid.setAttribute(Qt.WA_TranslucentBackground)
		self.parent.Dashboard.addDockWidget(Qt.RightDockWidgetArea, wid)
		wid.setFloating(True)

		self.close()

