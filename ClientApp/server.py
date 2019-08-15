from qt.serverwindow import *
from PyQt5.QtCore import Qt
import os
import time

hostname = "192.168.1.49"

class serverping(QtCore.QThread):
	checkreturnmsg = QtCore.pyqtSignal([str],[unicode])
	def __init__(self):
		super(serverping, self).__init__()
		self.response = None
		self._stop = False
	def run(self):
		while(not self._stop):
			self.response = os.system("ping -c 1 "+ hostname)
			self.checkreturnmsg.emit("checkreturnmsg")
			time.sleep(0.1)
	def stop(self):
		self.threadactive = False
		self._stop = True
		self.wait()

class ServerWindow(QtWidgets.QWidget, Ui_ServerWindow):
	def __init__(self, client, parent = None):
		super(ServerWindow, self).__init__()
		self.client = client
		self.setupUi(self)

		self.pingthread = serverping()
		self.pingthread.checkreturnmsg.connect(self.checkping)

		self.IPText.setText(self.client.host)
		self.client.data.checkserver_msg.connect(self.checkserver_msg)
		self.Back.clicked.connect(self.close)
		self.ConnectServer.clicked.connect(self.connect_server)
		self.DisconnectServer.clicked.connect(self.disconnect_server)
		self.Ping.clicked.connect(self.ping)
		self.StopPing.clicked.connect(self.stopping)
		#self.DisconnectServer.clicked.connect(self.disconnect_server)

	def ping(self):
		self.pingthread.start()
	def stopping(self):
		self.pingthread.stop()

	def checkping(self):
		if self.pingthread.response == 0:
			self.outputserver("Server is reachable, click connect\n")
			self.stopping()
		else:
			self.outputserver("Server is unreachable, ping again\n")


	def connect_server(self):
		err = self.client.attemptconnect()
		if err != None: self.outputserver(err)

	def disconnect_server(self):
		err = self.client.disconnect()
		if err != None: self.outputserver(err)

	def checkserver_msg(self):
		self.outputserver(self.client.data.client_msg)

	def outputserver(self, text):
		self.ServerOutput.moveCursor(QtGui.QTextCursor.End)
		self.ServerOutput.ensureCursorVisible()
		self.ServerOutput.append(text)