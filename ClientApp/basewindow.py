from PyQt5 import QtCore, QtGui, QtWidgets


#BaseWindow that is inherited from all windows. 
#Overrides basic functions like close and show
#Implements Fullscreen flags, cleaning up code in the individual windows
class BaseWindow(QtWidgets.QWidget):
	def __init__(self, parent = None):
		super(BaseWindow,self).__init__()
		self.fullscreen = False
		self.parent = parent
		self.notification = None
		self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
		if(parent != None and self.parent.fullscreen):
			self.fullscreen = True
			self.setWindowState(self.windowState() | QtCore.Qt.WindowFullScreen)

	def back(self):
		self.parent.show()
		self.close()

	def show(self):
		self.move(QtWidgets.qApp.desktop().availableGeometry().center() - self.rect().center())
		super(BaseWindow,self).show()

		#Display notification if there is a notification object present AND
		#If the window is the main window or if the notificaiton is not visible. 
		if(self.notification != None):
			self.notification.parent = self
			self.notification.show()
			# self.notification.activateWindow()
			# print(self.notification.visibleRegion().isEmpty())

			