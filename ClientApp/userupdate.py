from builtins import str
from qt.userupdatewindow import *
from PyQt5.QtCore import Qt
from github import Github
from git import Repo


class UserUpdateWindow(QtWidgets.QWidget, Ui_UserUpdate):
    def __init__(self, parent=None):
        super(UserUpdateWindow, self).__init__()
        self.setupUi(self)

        self.app = QtWidgets.QApplication.instance()

        # Make the selection Behavior as selecting the entire row
        self.SoftwareList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.SoftwareList.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        # Hide the vertical header which contains the Index of the row.
        self.SoftwareList.verticalHeader().hide()
        # Stretch out the horizontal header to take up the entire view
        header = self.SoftwareList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        temp = self.CurrentVersion.text()+ " " + self.app.applicationVersion()
        self.CurrentVersion.setText(temp)

        self.Back.clicked.connect(self.close)
        self.CheckUpdate.clicked.connect(self.checkupdate)
        self.Update.clicked.connect(self.update)
        # self.Rollback.clicked.connect(self.rollback)

    def checkupdate(self):
        token = "3a2f5c456fdda069efe987b19c3f6ed58c69aa37"
        github = Github(token)
        repo = github.get_repo("plloppii/DashboardApp")
        tags = repo.get_tags()
        self.SoftwareList.setRowCount(0)
        for t in tags:
            print(t.name, " date:", t.commit.last_modified)
            rowpos = self.SoftwareList.rowCount()
            self.SoftwareList.insertRow(rowpos)
            version = QtWidgets.QTableWidgetItem(t.name)
            version.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            date = QtWidgets.QTableWidgetItem(t.commit.last_modified)
            date.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.SoftwareList.setItem(rowpos,0,version)
            self.SoftwareList.setItem(rowpos,1,date)
            
    def update(self):
        software = self.SoftwareList.currentRow()
        selected_version = self.SoftwareList.item(software, 0)
        if selected_version != None:
            self.print_debug("Updating....")
        else:
            self.print_debug("Select a Version on list")

    def print_debug(self, text):
        self.DebugOutput.moveCursor(QtGui.QTextCursor.End)
        self.DebugOutput.ensureCursorVisible()
        self.DebugOutput.append(text)

