from builtins import str
from qt.userupdatewindow import *
from PyQt5.QtCore import Qt
from github import Github


class UserUpdateWindow(QtWidgets.QWidget, Ui_UserUpdate):
    def __init__(self, parent=None):
        super(UserUpdateWindow, self).__init__()
        self.setupUi(self)


        
        # Make the selection Behavior as selecting the entire row
        self.SoftwareList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.SoftwareList.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        # Hide the vertical header which contains the Index of the row.
        self.SoftwareList.verticalHeader().hide()
        # Stretch out the horizontal header to take up the entire view
        header = self.SoftwareList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)




        self.Back.clicked.connect(self.close)
        # self.CheckUpdate.clicked.connect(self.checkupdate)
        # self.Update.clicked.connect(self.update)
        # self.Rollback.clicked.connect(self.rollback)
