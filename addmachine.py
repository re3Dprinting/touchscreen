from qt.addmachinewindow import *
from Server.gigabotclient import *
from PySide2.QtCore import Qt


#   AddMachineWindow implemented the QtDesigner generated class, Ui_addmachine
class AddMachineWindow(QtWidgets.QWidget, Ui_addmachine):
#   Pass in the list of gigabotclient objects that contain data on gigabot.
#   Pass in the parent so that the addmachinewindow can be set as a Qt.Tool
    def __init__(self, gigabotthreads, parent = None):
        super(AddMachineWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.Tool)

        self.main = parent
        self.gigabotthreads = gigabotthreads

#       Move Window to Middle of Screen
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

#       Make the selection Behavior as selecting the entire row
        self.Devices.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
#       Hide the vertical header which contains the Index of the row.
        self.Devices.verticalHeader().hide()
#       Stretch out the horizontal header to take up the entire view
        header = self.Devices.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        rowpos = self.Devices.rowCount()

#       Populate the QTable with the avalible gigabots. 
        self.refreshtable()

#       Connect the ok button to retrieving the gigabot.
        ok = self.Button.button(QtWidgets.QDialogButtonBox.Ok)
        ok.clicked.connect(self.addmod)
#       Connecting the Quit Button to quiting.
        close = self.Button.button(QtWidgets.QDialogButtonBox.Cancel)
        close.clicked.connect(self.close)
        self.Refresh.clicked.connect(self.refreshtable)

#   Given the list of gigabots, display each IP address.
    def refreshtable(self):
        self.Devices.setRowCount(0)
        if len(self.gigabotthreads)>0:
            for t in self.gigabotthreads:
                #print t.ipaddress+ " : widgetlinked:", t.widgetlinked, " connected: ", t.connected, " Widget show: ", t.widgetshow
                #if (t.connected and t.widget == None) or (t.connected and not t.widget.isVisible()):
                if t.connected and (t.widget == None or not t.widget.isVisible()):
                #show up on table if a widget is not linked, or (is connected and widgetshow)
                    rowpos = self.Devices.rowCount()
                    self.Devices.insertRow(rowpos)
                    ip= QtWidgets.QTableWidgetItem(t.gigabot.ipaddress)
                    ip.setFlags( Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    num= QtWidgets.QTableWidgetItem(t.gigabot.idnum)
                    model = QtWidgets.QTableWidgetItem(t.gigabot.model)
                    self.Devices.setItem(rowpos, 0, model)
                    self.Devices.setItem(rowpos, 1, ip)
                    self.Devices.setItem(rowpos, 2, num)

#   Add a Module after a row is selected
#   If the Gigabotnumber is inputted, link the number to the gigabot object. 
    def addmod(self):
        if(len(self.gigabotthreads) >0):
            selected = self.Devices.currentRow()
            selectedip = self.Devices.item(selected,1)
            gigabot = None
            for t in self.gigabotthreads:
                if t.ipaddress == selectedip.text():
                    thread = t
            gigabotnum = self.Devices.item(selected,2)
            if gigabotnum and len(gigabotnum.text()) != 0: thread.gigabot.idnum= gigabotnum.text()

            self.main.addModule(thread)
        #self.close()
