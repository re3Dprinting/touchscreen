from qt.dashboardwindow import *
from addmachine import *
from modulegigabot import *
from Server.gigabotclient import *


#   DashboardWindow class
class DashboardWindow(QtWidgets.QMainWindow, Ui_DashboardWindow):
    def __init__(self, view_thread, server_thread):
        super(DashboardWindow,self).__init__()
        self.setupUi(self)
#       List of module widgets to be stored

#       Thread that updates the modules
#       connects the two sinals to two functions, updateall and checkvisible
        self.viewupdater = view_thread
        self.viewupdater.update.connect(self.updateall)
        self.viewupdater.checkvisible.connect(self.checkvisible)
        self.viewupdater.start()
#       Server thread that starts or stops the server
        self.serverthread = server_thread
        self.serverthread.start()

        self.handler = self.serverthread.handler
        self.gigabots = self.handler.gigabots

        self.gigabots.append(gigabotclient("192.168.1.169"))
#       self.gigabots.append(gigabotclient("192.168.1.151"))
#       self.gigabots.append(gigabotclient("192.168.1.49"))
#       self.gigabots.append(gigabotclient("192.168.1.12"))

#       Set the Dashboard as a MainWindow Object so a DockWidget can be nested inside.
        self.Dashboard = QtWidgets.QMainWindow()
        self.Dashboard.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks)
#       Set the sizePolicy so that the application is responsive
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Dashboard.sizePolicy().hasHeightForWidth())
        self.Dashboard.setSizePolicy(sizePolicy)
#       Add the MainWindow back into the layout
        self.gridLayout.addWidget(self.Dashboard, 2, 0, 1, 1)
        self.showMaximized()

#       Connect the Menu Items to the appropriate functions
        self.AddMachine.triggered.connect(self.add_machine)
        self.Quit.triggered.connect(self.closeall)
        self.StartServer.clicked.connect(self.startserv)
        self.StopServer.clicked.connect(self.stopserv)

    def closeall(self):
        self.handler.quit()
        #send all data to database
        self.close()
    def add_machine(self):
        self.pop = AddMachineWindow(self.gigabots, self)
        self.pop.show()
    def startserv(self):
        self.serverthread.startflag = True
        self.ServerStatus.setText("Server is Running...")
    def stopserv(self):
        self.serverthread.stopflag = True
        self.ServerStatus.setText("Server is Disconnected")

    def addModule(self, gigabot):
        if not gigabot.widgetlinked:
            mod = ModuleGigabot(gigabot)
            wid = QtWidgets.QDockWidget(self)
            wid.setWidget(mod)
            gigabot.widget = wid
            gigabot.mod = mod
            gigabot.widgetlinked = True

            gigabot.widget.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
            #self.wid.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetClosable)
            #self.wid.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
            gigabot.widget.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable)
            #wid[i].setWindowFlags(Qt.FramelessWindowHint)
            gigabot.widget.setAttribute(Qt.WA_TranslucentBackground)
            self.Dashboard.addDockWidget(Qt.RightDockWidgetArea,gigabot.widget)
            gigabot.widget.setFloating(True)
            gigabot.widgetshow = True
        if not gigabot.widgetshow:
            gigabot.widget.show()

#   Slots that are called periodically by view thread in qtmain.py
    def updateall(self):
        for g in self.gigabots:
            if g.widget != None:
                g.mod.update_all()
    def checkvisible(self):
        for g in self.gigabots:
            if g.widget != None and not g.widget.isVisible():
                g.widgetshow = False


       # Determine the size of the window
       #  sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
       #  wid = sizeObject.width()
       #  hei = sizeObject.height()
       #  self.resize( wid-100, hei-100)