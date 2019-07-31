# This Python file uses the following encoding: utf-8
import sys

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from dashboard import *
from Server.server_main import serverhandler
import time
import threading

#   Server Thread used to handle the blocking server call, listen_for_clients()
#   This Thread spawns other Threads for each Client connected.
#   Also handles when to start and stop the server. 
class server_thread(QtCore.QThread):
    def __init__(self, handler, parent = None):
        QtCore.QThread.__init__(self,parent)
        self.handler= handler
        self.startflag = False
        self.stopflag = False
        self.listen = False
        self.newclientconnected = False
    def run(self):
        while(True):
            if self.startflag: 
                self.handler.startserver()
                self.listen = True
                self.startflag = False
            if self.stopflag:
                self.handler.stopserver()
                self.listen = False
                self.stopflag = False
            if self.listen: 
                self.handler.listen_for_clients()

#   View Thread, that updates the view whenever new data comes in from the server side.
#   Contains two counters, one to handle updating the modules
#   second to handle checking if the modules are visible. 
class view_thread(QtCore.QThread):
    update = QtCore.Signal([str],[unicode])
    checkvisible = QtCore.Signal([str],[unicode])
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self,parent)
        self.count = [0,0]
    def run(self):
        while(True):
            self.count[0] +=1
            self.count[1] +=1
            if self.count[1] >= 5: 
                self.update.emit("updateall")
                self.count[1] = 0
            if self.count[0] >= 2: 
                self.checkvisible.emit("checkvisible")
                self.count[0] = 0
            time.sleep(0.2)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

#   Start Server Handler
    serv_handler = serverhandler()
#   The ViewThread created to update the mainwindow
    viewthread = view_thread()
#   The ServerThread created to handle server calls
    serverthread = server_thread(serv_handler)
#   Main Dashboard Window
    dashboardwindow = DashboardWindow(viewthread, serverthread)

    dashboardwindow.show()

    app.exec_()
