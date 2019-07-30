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
class server_thread(QtCore.QThread):
    serverstatus = QtCore.Signal([str],[unicode])
    def __init__(self, handler, parent = None):
        QtCore.QThread.__init__(self,parent)
        self.handler= handler
        self.startflag = False
        self.stopflag = False
        self.listen = False
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
            if self.listen: self.handler.listen_for_clients()

#   View Thread, that updates the view whenever new data comes in from the server side.
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
            if self.count[1] >= 10: 
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

    viewthread = view_thread()
    serverthread = server_thread(serv_handler)
#   Main Dashboard Window
    dashboardwindow = DashboardWindow(viewthread, serverthread)

    # serv_thread = server_thread(serv_handler)
    # serv_thread.start()

    dashboardwindow.show()

    app.exec_()
    #sys.exit(app.exec_())


    #        mods = []
    #        dockwids = []
    #        for i in range(6):
    #            mods.append(GigabotModule(str(i)))
    #            dockwids.append(QtWidgets.QDockWidget(self))
    #        for i in range(6):
    #            dockwids[i].setWidget(mods[i])
    #            dockwids[i].setFeatures(QtWidgets.QDockWidget.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetClosable)
    #            dockwids[i].setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
    #            #dockwids[i].setWindowFlags(Qt.FramelessWindowHint)
    #            dockwids[i].setAttribute(Qt.WA_TranslucentBackground)
    #            dockwids[i].setFloating(True)
    #        for i in range(6):
    #            self.Dashboard.addDockWidget(Qt.NoDockWidgetArea,dockwids[i])
