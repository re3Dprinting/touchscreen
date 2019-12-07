#!/usr/bin/python3.4

from builtins import str
from qt.userupdatewindow import *
from PyQt5.QtCore import Qt
# from github import Github
from git import Repo
from git import Git
import os
import psutil
from pathlib import Path
import time
import sys


class UserUpdateWindow(QtWidgets.QWidget, Ui_UserUpdate):
    def __init__(self, personality, parent=None):
        super(UserUpdateWindow, self).__init__()
        self.setupUi(self)

        self.personality = personality
        self.app = QtWidgets.QApplication.instance()

        self.current_path = Path(__file__).parents

        #Get the current path (local repository) and make sure that the github link is the current repository.
        self.git = Git(self.current_path[1].__str__())
        self.repo = Repo(self.current_path[1].__str__())

        found_remote = False
        #Check if re3d remote repository is in current remote tree
        for r in self.repo.remotes:
            if r.name == "re3d":
                self.remote_repo = r
                found_remote = True
            else: self.repo.delete_remote(r) 
        #If re3d repo does not exist, add it as a remote.
        if not found_remote:
            self.remote_repo = self.repo.create_remote("re3d", "https://github.com/re3Dprinting/touchscreen")
            # self.remote_repo = self.repo.create_remote("re3d", "https://github.com/plloppii/DashboardApp.git")

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

    def checkupdate(self):
        #Fetch all of the tags from the remote repository.
        for tag in self.repo.tags:
            self.repo.delete_tag(tag)

        self.remote_repo.fetch("--tags")
        tags = self.repo.tags

        self.SoftwareList.setRowCount(0)

        for t in tags:
            if("release" in t.name and not self.app.applicationVersion() in t.name):
                tag_date = time.asctime(time.gmtime(t.commit.committed_date))
                print(t.name, " date:", tag_date)
                rowpos = self.SoftwareList.rowCount()
                self.SoftwareList.insertRow(rowpos)
                version = QtWidgets.QTableWidgetItem(t.name.strip("release/"))
                version.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                date = QtWidgets.QTableWidgetItem(tag_date)
                date.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.SoftwareList.setItem(rowpos,0,version)
                self.SoftwareList.setItem(rowpos,1,date)
        if(self.SoftwareList.rowCount() == 0): 
            self.print_debug("No software versions found. The server might be down, please try again later.")

    def update(self):
        software = self.SoftwareList.currentRow()
        selected_version = self.SoftwareList.item(software, 0)
        if selected_version != None and selected_version.text() != self.app.applicationVersion():
            self.print_debug("Updating....")
            #checkout into new tag and run a script.
            #script will reboot device and properly shut down Raspberry pi.
            
            self.git.checkout("release/" + selected_version.text())
            if(self.personality.fullscreen == False): self.restart_program("jtmain.py")
            else: self.restart_program("qtmain.py")
        elif selected_version == self.app.applicationVersion():
            self.print_debug("Currently on that software version")
        else:
            self.print_debug("Select a Version on list")

    def print_debug(self, text):
        self.DebugOutput.moveCursor(QtGui.QTextCursor.End)
        self.DebugOutput.ensureCursorVisible()
        self.DebugOutput.append(text)

    def restart_program(self, argument):
        # Restarts the current program, with file objects and descriptors cleanup
        try:
            p = psutil.Process(os.getpid())
            for handler in p.open_files() + p.connections():
                os.close(handler.fd)
        except Exception as e:
            logging.error(e)

        python = sys.executable
        os.execl(python, python, argument)

    #  #Script to edit the bashscript on the raspberry pi if necessary.    
    # def editbashscript(self, new_version):
    #     script_path = Path(__file__).parents[2].__str__()
    #     script_file = "/StartClientApp.sh"
    #     # print(script_path+script_file+ os.path.isfile(script_path+ script_file))
    #     if not os.path.isfile(script_path+ script_file):
    #         self.print_debug("Cannot locate script path: "+ script_path+ script_file)
    #         return False
    #     else:
    #         for line in open(script_path+script_file):
    #             tmp = line.split(" ")
    #             if("cd" in tmp): 
    #                 tmp1 = tmp[1].split("/")
    #                 i = tmp1.index("DashboardApp_"+ self.app.applicationVersion)
    #                 tmp1[i] = "DashboardApp_"+ new_version
    #                 tmp[1] = tmp1
    #                 line = " ".join(tmp)
    #             if("python" in tmp):
    #                 tmp[0] = "python3"
    #                 line = " ".join(tmp)
    #         return True
