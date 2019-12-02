from builtins import str
from qt.userupdatewindow import *
from PyQt5.QtCore import Qt
from github import Github
from git import Repo
import os
import shutil
from pathlib import Path


class UserUpdateWindow(QtWidgets.QWidget, Ui_UserUpdate):
    def __init__(self, parent=None):
        super(UserUpdateWindow, self).__init__()
        self.setupUi(self)

        self.app = QtWidgets.QApplication.instance()

        #If the Application folder name does not have the version in it, append the version number.
        self.old_path_tmp = Path(__file__).parents[1].__str__()
        file_names = self.old_path_tmp.split("/")
        if("DashboardApp" in file_names): 
            i = file_names.index("DashboardApp")
            file_names[i] += "_"+self.app.applicationVersion()
            self.old_path = "/".join(file_names)
            os.rename(self.old_path_tmp, self.old_path)
        else:
            self.old_path = "/".join(file_names)

        self.update_path = Path(__file__).parents[2].__str__()+ "/DashboardApp_"

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
        if(os.path.isfile(Path(__file__).parents[1].__str__()+ "/git.token")):
            token = open(Path(__file__).parents[1].__str__()+ "/git.token").read()
        else: 
            self.print_debug("Token not found! Cannot fetch software versions")
            return
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
        if selected_version != None and selected_version != self.app.applicationVersion():
            self.print_debug("Updating....")
            self.update_path += selected_version
            self.copy_and_rename()
            update_repo = git.Repo(self.update_path)
            update_repo.fetch()
            update_repo.checkout(selected_version)
            #Change Bashscript to boot up to newly pulled version.
            editbashscript(selected_version)

        elif selected_version == self.app.applicationVersion():
            self.print_debug("Currently on that software version")
        else:
            self.print_debug("Select a Version on list")

    def print_debug(self, text):
        self.DebugOutput.moveCursor(QtGui.QTextCursor.End)
        self.DebugOutput.ensureCursorVisible()
        self.DebugOutput.append(text)

    def copy_and_rename(self):
        try:
            shutil.copytree(self.old_path,self.update_path)
        # Directories are the same
        except shutil.Error as e:
            print('Directory not copied. Error: %s' % e)
        # Any error saying that the directory doesn't exist
        except OSError as e:
            print('Directory not copied. Error: %s' % e)
    def editbashscript(self, new_version):
        script_path = Path(__file__).parents[2].__str__()
        script_file = "/StartClientApp.sh"
        if os.path.isfile(script_path+ script_file):
            for line in open(script_path+script_file):
                tmp = line.split(" ")
                if("cd" in tmp): 
                    tmp1 = tmp[1].split("/")
                    i = tmp1.index("DashboardApp_"+ self.app.applicationVersion)
                    tmp1[i] = "DashboardApp_"+ new_version
                    tmp[1] = tmp1
                    line = " ".join(tmp)
                if("python" in tmp):
                    tmp[0] = "python3"
                    line = " ".join(tmp)
