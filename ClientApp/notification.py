
from qt.notificationwindow import Ui_NotificationWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class Notification(QtWidgets.QWidget, Ui_NotificationWindow):
	def __init__(self, parent=None):
		super(Notification, self).__init__()
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
		parent_rect = parent.rect()
		# print(parent.geometry().width())
		notification_width = parent.geometry().width() *3/5
		notification_height = notification_width/6
		self.resize(notification_width, notification_height)

		# self.NotificationWindow.resize()

		print(parent_rect.left(), parent_rect.top())
		print(self.mapToGlobal(parent.pos()) )


		tmp = parent.geometry().width()/5
		notification_pos = QtCore.QPoint(parent_rect.left() + tmp, parent_rect.top()-self.geometry().height()+5)
		notification_pos = parent.mapToGlobal(notification_pos)
		# print(parent_rect.left() + tmp, parent_rect.top()-self.geometry().height()+5)
		# print(notification_pos)
		self.move(notification_pos)
		print(self.mapToGlobal(self.pos()) )
		# parent_width = parent.width()
		# parent_length = parent.length()

        