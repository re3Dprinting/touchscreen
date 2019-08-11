from qt.serverwindow import *
from PyQt5.QtCore import Qt

class ServerWindow(QtWidgets.QWidget, Ui_ServerWindow):
	def __init__(self, client, parent = None):
		super(ServerWindow, self).__init__()
		self.client = client
		self.setupUi(self)

		self.Back.clicked.connect(self.close)
		self.ConnectServer.clicked.connect(self.connect_server)
		#self.DisconnectServer.clicked.connect(self.disconnect_server)

	def connect_server(self):
		err = self.client.attemptconnect()
		if err != None: self.outputserver(err)


	# def disconnect_server(self):
	# 	self.

	def outputserver(self, text):
		self.ServerOutput.moveCursor(QtGui.QTextCursor.End)
		self.ServerOutput.ensureCursorVisible()
		self.ServerOutput.append(text)