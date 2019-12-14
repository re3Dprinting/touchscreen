
from qt.notificationwindow import Ui_NotificationWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class Notification(QtWidgets.QWidget, Ui_NotificationWindow):
	def __init__(self, parent=None):
		super(Notification, self).__init__()
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
		# parent_width = parent.width()
		# parent_length = parent.length()

        