# This Python file uses the following encoding: utf-8
import sys

from PySide2 import QtCore, QtGui, QtWidgets
from mainwindow import *
from Server.server_main import serverhandler
import time

#class dashboard(QtWidgets.QWidget):
#    def __init__(self, parent= None):
#        QtWidgets.QWidget.__init__(self,parent)
#        self.setGeometry(200,200,1080,720)
#        self.runpyscript = QtWidgets.QPushButton("Add Machine",self)
#        self.runpyscript.setGeometry(10,10,150,30)
#        self.runpyscript.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

#        self.connect(self.runpyscript, QtCore.SIGNAL("clicked()"),
#                    QtWidgets.qApp, QtCore.SLOT("quit()"))
class server_thread(QtCore.QThread):
    def __init__(self, handler, parent = None):
        QtCore.QThread.__init__(self,parent)
        self.handler= handler
    def run(self):
        while(True):
            self.handler.listen_for_clients()

class view_thread(QtCore.QThread):
    def __init__(self, serv_handler, view, parent=None):
        QtCore.QThread.__init__(self,parent)
        self.view = view
        self.serv_handler = serv_handler
    def run(self):
        while(True):
            #self.serv_handler.listen_for_clients()
            # print self.serv_handler.gigabotthreads[0].printstuff
            # print "I am moving"
            if len(self.serv_handler.gigabotthreads): 
                serv_handler.message = self.serv_handler.gigabotthreads[0].printstuff
                self.serv_handler.gigabotthreads[0].printstuff = ""
            if self.serv_handler.message != "":
                self.view.refresh_text_box(self.serv_handler.message)
                self.serv_handler.message = ""
                
            #else: self.view.refresh_text_box("ping")
            QtWidgets.QApplication.processEvents()
            time.sleep(0.5)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)

    def refresh_text_box(self, astring):
        self.Serveroutput.append(astring)
        QtWidgets.QApplication.processEvents()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dashboardwindow = MainWindow()

    serv_handler = serverhandler()
    serv_thread = server_thread(serv_handler)

    view_object = view_thread(serv_handler, dashboardwindow)

    serv_thread.start()
    view_object.start()

    dashboardwindow.show()

    app.exec_()
    #sys.exit(app.exec_())
