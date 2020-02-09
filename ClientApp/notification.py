
from qt.notificationwindow import Ui_NotificationWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class Notification(QtWidgets.QWidget, Ui_NotificationWindow):
	def __init__(self, text, parent=None):
		super(Notification, self).__init__()
		self.setupUi(self)
		self.setWindowFlags(self.windowFlags() |  QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
		
		self.Text.setText(text)
		self.parent = parent
		self.Close.clicked.connect(self.close)

		

	def show(self):
		if(self.parent != None): 
			parent_rect = self.parent.rect()
			notification_width = self.parent.geometry().width() *3/5
			notification_height = notification_width/6
			self.resize(notification_width, notification_height)

			tmp = self.parent.geometry().width()/5

			notification_pos = QtCore.QPoint(parent_rect.left() + tmp, parent_rect.bottom() - self.geometry().height())
			notification_pos = self.parent.mapToGlobal(notification_pos)
			self.move(notification_pos)
		# super(Notification,self).activateWindow()
		super(Notification,self).show()

	def close(self):
		self.parent.notification = None
		self.parent = None
		super(Notification,self).close()

