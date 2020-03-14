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
        self.debug = (self.properties["debug"] == "true")

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
        #If re3d repo does not exist, add it as a remote.
        if not found_remote:
            self.remote_repo = self.repo.create_remote("re3d", "https://github.com/re3Dprinting/touchscreen")
            # self.remote_repo = self.repo.create_remote("re3d", "https://github.com/plloppii/DashboardApp.git")

        # Make the selection Behavior as selecting the entire row
        self.SoftwareList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.SoftwareList.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        # Update the side dialog box when a software version is selected. 
        self.SoftwareList.itemSelectionChanged.connect(self.show_tag_message)
        # Hide the vertical header which contains the Index of the row.
        self.SoftwareList.verticalHeader().hide()
        # Stretch out the horizontal header to take up the entire view
        header = self.SoftwareList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        #  Append the version to the current version window. 
        temp = self.CurrentVersion.text()+ " " + self.app.applicationVersion()
        self.CurrentVersion.setText(temp)

        self.Back.clicked.connect(self.back)
        self.CheckUpdate.clicked.connect(self.checkupdate)
        self.Update.clicked.connect(self.update)

    def checkupdate(self):
        #Fetch all of the tags from the remote repository.
        try:
            # WHY delete other tags??? No, bad code.
            # Check if tags can be updated without deleting them. 
            # for tag in self.repo.tags:
            #    self.repo.delete_tag(tag)

            self.remote_repo.fetch("--tags")
            tags = self.repo.tags
            tags.reverse()

            self.SoftwareList.setRowCount(0)

            # Check each tag and if it is a "release" tag. 
            # Append the tag to the list on the table widget. 
            self.current_tags = []
            for t in tags:
                if("release" == t.name.split("/")[0]): #and not self.app.applicationVersion() in t.name #<--- Dont show current version
                    self.current_tags.append(t)
                    tag_date = time.strftime('%I:%M%p %m/%d/%y', time.localtime(t.commit.committed_date))

                    #Strip out the release/ part of the tag. 
                    ver = t.name.lstrip("release/")

                    #Attempt to split up the current version and given version into three vars in an array
                    current_v = self.app.applicationVersion().split(".")
                    given_v = ver.split(".")

                    #Check for an update if and only if the current version and given version both follow the X.X.X sematic versioning. 
                    if(len(current_v) == 3 and len(given_v) == 3):
                        #Check if there is a newer software version avalible. 
                        self.checkagainstcurrent(current_v, given_v)
                    
                    #Show tag only if the given tag is following X.X.X OR if debug mode is turned on. 
                    if(self.debug or len(given_v) == 3):
                        rowpos = self.SoftwareList.rowCount()
                        self.SoftwareList.insertRow(rowpos)
                        version = QtWidgets.QTableWidgetItem(t.name.lstrip("release/"))

                        version.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                        date = QtWidgets.QTableWidgetItem(tag_date)
                        date.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                        self.SoftwareList.setItem(rowpos,0,version)
                        self.SoftwareList.setItem(rowpos,1,date)
            # If no versions are found, push a debug message to the window. 
            # If there is a newer version avalible, create a notification object and return it to be caught by the window. 
            if(self.SoftwareList.rowCount() == 0): self.print_debug("No software versions found. The server might be down, please try again later.")
            elif(self.new_version_avalible):
                return Notification("A new software version is available!\nTo update, go to Settings > Software Update")
        except Exception as e:
            print(e)

    # Check if there is a newer software version avalible. 
    def checkagainstcurrent(self, current_version, given_version):
        for i in range(len(current_version)):
            if(int(current_version[i]) < int(given_version[i])):
                self.new_version_avalible = True
                return

    #Grab the tag message and display it. 
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
    
    def print_debug(self, text):
        self.DebugOutput.append(text)
    
    # Restart the program by using psutil. Grab the PID of the python application and kill it. 
    def restart_program(self, argument):
        try:
            p = psutil.Process(os.getpid())
            for handler in p.open_files() + p.connections():
                os.close(handler.fd)
        except Exception as e:
            logging.error(e)

        #Restart the program with the original arguments and python executable. 
        python = sys.executable
        os.execl(python, python, argument)

