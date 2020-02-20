#!/usr/bin/python3.4

from builtins import str
from qt.userupdatewindow import Ui_UserUpdate
from notification import Notification
from basewindow import BaseWindow

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

from git import Repo
from git import Git
import os
import psutil
from pathlib import Path
import time
import sys


class UserUpdateWindow(BaseWindow, Ui_UserUpdate):
    def __init__(self, personality, parent=None):
        super(UserUpdateWindow, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.personality = personality
        self.app = QtWidgets.QApplication.instance()
        self.new_version_avalible = False

        tmp_path = Path(__file__).parent.absolute()
        # print(tmp_path)
        self.current_path = Path(os.path.realpath(tmp_path)).parent
        # print(self.current_path.__str__())

        #Get the current path (local repository) and make sure that the github link is the current repository.
        self.git = Git(self.current_path.__str__())
        self.repo = Repo(self.current_path.__str__())
        self.current_tags = None

        found_remote = False
        #Check if re3d remote repository is in current remote tree
        for r in self.repo.remotes:
            if r.name == "re3d":
                self.remote_repo = r
                found_remote = True
            # Why delete existing remotes? This is a hostile act.
            # else: self.repo.delete_remote(r) 
        #If re3d repo does not exist, add it as a remote.
        if not found_remote:
            self.remote_repo = self.repo.create_remote("re3d", "https://github.com/re3Dprinting/touchscreen")
            # self.remote_repo = self.repo.create_remote("re3d", "https://github.com/plloppii/DashboardApp.git")

        # Make the selection Behavior as selecting the entire row
        self.SoftwareList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.SoftwareList.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.SoftwareList.itemSelectionChanged.connect(self.show_tag_message)
        # Hide the vertical header which contains the Index of the row.
        self.SoftwareList.verticalHeader().hide()
        # Stretch out the horizontal header to take up the entire view
        header = self.SoftwareList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        temp = self.CurrentVersion.text()+ " " + self.app.applicationVersion()
        self.CurrentVersion.setText(temp)

        self.Back.clicked.connect(self.back)
        self.CheckUpdate.clicked.connect(self.checkupdate)
        self.Update.clicked.connect(self.update)

    def checkupdate(self):
        #Fetch all of the tags from the remote repository.
        try:
            # WHY delete other tags??? No, bad code.
            # for tag in self.repo.tags:
            #    self.repo.delete_tag(tag)

            self.remote_repo.fetch("--tags")
            tags = self.repo.tags
            tags.reverse()

            self.SoftwareList.setRowCount(0)

            self.current_tags = []
            for t in tags:
                if("release" == t.name.split("/")[0]): #and not self.app.applicationVersion() in t.name #<--- Dont show current version
                    self.current_tags.append(t)
                    tag_date = time.strftime('%I:%M%p %m/%d/%y', time.localtime(t.commit.committed_date))
                    rowpos = self.SoftwareList.rowCount()
                    self.SoftwareList.insertRow(rowpos)
                    version = QtWidgets.QTableWidgetItem(t.name.strip("release/"))
                    self.checkagainstcurrent(t.name.strip("release/"))
                    version.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                    date = QtWidgets.QTableWidgetItem(tag_date)
                    date.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.SoftwareList.setItem(rowpos,0,version)
                    self.SoftwareList.setItem(rowpos,1,date)
            if(self.SoftwareList.rowCount() == 0): self.print_debug("No software versions found. The server might be down, please try again later.")
            elif(self.new_version_avalible):
                return Notification("A new software version is available!\nTo update, go to Settings > Software Update")
        except Exception as e:
            print(e)

    def show_tag_message(self):
        item = self.SoftwareList.currentRow()
        selected = self.SoftwareList.item(item, 0)
        if(selected != None):
            self.DebugOutput.clear()
            self.print_debug("re:3Display "+ selected.text() + " changelog:\n")
            version = "release/"+ selected.text()
            for tag in self.current_tags:
                if(version == tag.name):
                    if tag.tag is None:
                        self.print_debug("(No description)")
                    else:
                        self.print_debug(tag.tag.message)
            self.DebugOutput.moveCursor(QtGui.QTextCursor.Start)
            self.DebugOutput.ensureCursorVisible()

#   Update function called by clicking the Update/Rollback button
#   Uses psutil to kill the current process, then reexecutes the original python command. 
    def update(self):
        software = self.SoftwareList.currentRow()
        selected_version = self.SoftwareList.item(software, 0)
        if selected_version != None: #and selected_version.text() != self.app.applicationVersion(): #<--- Dont allow update to current version
            self.print_debug("Updating....")

            self.git.checkout("release/" + selected_version.text())
            if(self.personality.fullscreen == False): self.restart_program(sys.argv[0])
            else: self.restart_program(sys.argv[0])
        else:
            self.print_debug("Select a Version on list")

    def checkagainstcurrent(self, version):
        current_v = self.app.applicationVersion().split(".")
        given_v = version.split(".")
        for i in range(len(current_v)):
            if(int(current_v[i]) < int(given_v[i])):
                self.new_version_avalible = True
                return
                
    def print_debug(self, text):
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

