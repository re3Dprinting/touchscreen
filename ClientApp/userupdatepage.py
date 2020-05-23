#!/usr/bin/python3.4

from builtins import str
import os
import psutil
import shutil
from pathlib import Path
import time
import sys
import logging

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets

from .fsutils.subfilesystem import SubFileSystem

import git

import zipfile, tarfile
from threading import Thread
from qt.userupdatepage_qt import Ui_UserUpdatePage
from notification import Notification
from basepage import BasePage
from util.load_properties import get_software_details


class UserUpdatePage(BasePage, Ui_UserUpdatePage):
    #Signal sent to notify ui is ready to be updated.
    ui_update_signal = pyqtSignal(str)
    unzip_progress = pyqtSignal(str,bool)

    def __init__(self, context):
        super(UserUpdatePage, self).__init__()

        self._logger = logging.getLogger(__name__)
        self._log("UserUpdate __init__")
        self.setupUi(self)

        self.personality = context.personality
        self.ui_controller = context.ui_controller
        self.properties = context.properties

        self.setbuttonstyle(self.Back)

        self.app = QtWidgets.QApplication.instance()
        self.new_version_avalible = False
        # self.debug = (self.properties["debug"] == "true")
        self.debug = True

        #Subdirectory object to check for USB software updates.
        self.subdir = SubFileSystem(self.personality.watchpoint)
        self.usb_mounted = False

        #Get the current path (local repository) and make sure that the github link is the current repository.       
        try:
            self.repo = git.Repo(self.personality.gitrepopath)
            self.git = git.Git(self.personality.gitrepopath)
            found_remote = False
            #Check if re3d remote repository is in current remote tree
            for r in self.repo.remotes:
                if r.name == "re3d":
                    self.remote_repo = r
                    found_remote = True
            #If re3d repo does not exist, add it as a remote.
            if not found_remote:
                self.remote_repo = self.repo.create_remote("re3d", "https://github.com/re3Dprinting/touchscreen")
        except Exception as e:
            print("userupdate: __init__() exception: ", e)

        self.update_Thread = None
        #Initialize the array for Git Software Updates and USB Software Updates
        self.git_updates = []
        self.usb_updates = []

        #Signal to notify that UI updates are ready from a thread
        self.ui_update_signal.connect(self.ui_update_list)
        #Signal passed to subfilesystem to update unzipping progress in UI
        self.unzip_progress.connect(self.display_stored_text)
        self.store_text= ""
            
        # Make the selection Behavior as selecting the entire row
        self.SoftwareList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.SoftwareList.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        # Update the side dialog box when a software version is selected. 
        self.SoftwareList.itemSelectionChanged.connect(self.show_update_message)
        # Hide the vertical header which contains the Index of the row.
        self.SoftwareList.verticalHeader().hide()
        # Stretch out the horizontal header to take up the entire view
        header = self.SoftwareList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.DebugOutput.setLineWrapMode(QtWidgets.QTextBrowser.NoWrap)

        #  Append the version to the current version window. 
        temp = self.CurrentVersion.text()+ " " + self.app.applicationVersion()
        self.CurrentVersion.setText(temp)

        self.Back.clicked.connect(self.back)
        self.CheckUpdate.clicked.connect(self.checkupdate)
        self.Update.clicked.connect(self.update)


    def checkupdate(self):
        self.CheckUpdate.setEnabled(False)
        self.DebugOutput.clear()
        self.store_text = ""
        self.SoftwareList.setRowCount(0)
        self.git_updates = []
        self.usb_updates = []
        self.display_stored_text("Fetching Server Updates...")

        self.update_Thread = Thread(target = self.checkupdate_handler)
        self.update_Thread.setDaemon(True)
        self.update_Thread.start()

    def checkupdate_handler(self):
        """
        Handler that is ran on a seperate thread, that checks the Git software updates first if Wifi is enabled
        Pushes the updates up to the UI if ready, then checks for USB updates. 
        Then pushes updates to the UI a second time. 
        """
        try:
            if(self.properties["wifienabled"]):
                self.check_git_software()
                self.ui_update_signal.emit("Server Updates found... \nFetching USB Updates...")
            self.check_usb_software()
            if(self.usb_updates): self.ui_update_signal.emit("USB Updates found.")
            else: self.ui_update_signal.emit("No USB Updates Found.")
            self.ui_update_signal.emit("setEnable")
        except Exception as e:
            print("userupdate: checkupdate() exception: ", e)

    def ui_update_list(self, msg):
        if(msg == "setEnable"):
            self.CheckUpdate.setEnabled(True)
            return
            
        self.display_stored_text(msg)
        self.SoftwareList.setRowCount(0)
        for u in self.usb_updates:
            rowpos = self.SoftwareList.rowCount()
            self.SoftwareList.insertRow(rowpos)
            version = QtWidgets.QTableWidgetItem(u.displayname)

            version.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            date = QtWidgets.QTableWidgetItem(u.timestamp)
            date.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.SoftwareList.setItem(rowpos,0,version)
            self.SoftwareList.setItem(rowpos,1,date)

        for t in self.git_updates:
            tag_date = time.strftime('%I:%M%p %m/%d/%y', time.localtime(t.commit.committed_date))
            #TODO Only show releases if it follows X.X.X
            rowpos = self.SoftwareList.rowCount()
            self.SoftwareList.insertRow(rowpos)
            version = QtWidgets.QTableWidgetItem(t.name)

            version.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            date = QtWidgets.QTableWidgetItem(tag_date)
            date.setFlags(Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.SoftwareList.setItem(rowpos,0,version)
            self.SoftwareList.setItem(rowpos,1,date)

        # If no versions are found, push a debug message to the window. 
        # If there is a newer version avalible, create a notification object and return it to be caught by the window. 
        if(self.SoftwareList.rowCount() == 0): self.display_text("No software versions found on server or on USB")
        if(self.new_version_avalible):
            return Notification("A new software version is available!\nTo update, go to Settings > Software Update")

    def check_git_software(self):
        #Delete tags if they contain "release/"
        for tag in self.repo.tags:
            if("release/" in tag.name or 
                "devel/" in tag.name or 
                "hotfix/" in tag.name):
                self.repo.delete_tag(tag)

        self.remote_repo.fetch("-tf")
        tags = sorted(self.repo.tags, key=lambda t: t.commit.committed_date)
        tags.reverse()

        #Grab the current version and check if it is a beta version. 
        current_v = self.app.applicationVersion()
        curr_isCustomerRelease = self.isCustomerRelease(current_v)

        # Check each tag and if it is a "release" tag. 
        # Append the tag to the list on the table widget. 
        self.git_updates = []
        for t in tags:
            #Grab the current Version and the given version and see if they are beta versions. 
            given_v = t.name
            given_isCustomerRelease = self.isCustomerRelease(given_v)

            #Skip over all tags that contain archive
            if("archive" in t.name): continue

            if( ("release" in t.name or
                    "devel" in t.name or 
                    "hotfix" in t.name) 
                and (not self.properties["permission"] == "developer")): continue

            if("beta" in t.name and not(self.properties["permission"] == "developer" or self.properties["permission"] =="beta-tester")): continue

            #Filter out any remaining tags that are not in the given X.X.X format. 
            if(self.properties["permission"] == "customer" and not given_isCustomerRelease): continue 

            self.git_updates.append(t)

            #Check for an update if and only if the current version and given version both follow the X.X.X sematic versioning. 
            if(curr_isCustomerRelease and given_isCustomerRelease):
                #Check if there is a newer software version avalible. 
                self.checkagainstcurrent(current_v, given_v)
    
    #Is Customer Release only if version is in format of X.X.X
    def isCustomerRelease(self, version):
        version = version.split(".")
        if(len(version) < 3): return False
        for v in version:
            if(not v.isdigit()):
                return False
        return True

    # Check if there is a newer software version avalible. 
    def checkagainstcurrent(self, current_version, given_version):
        current_version = current_version.split(".")
        given_version = given_version.split(".")
        for i in range(len(current_version)):
            if(int(current_version[i]) < int(given_version[i])):
                self.new_version_avalible = True
                return

    def show_update_message(self):
        """
        Callback when a item in the updates list is selected.
        Determines if it is a USB or Git update. Shows changelog from file(USB Update) or Git tag message
        """
        item = self.SoftwareList.currentRow()
        selected = self.SoftwareList.item(item, 0)
        if(selected != None):
            self.DebugOutput.clear()
            selected_update = selected.text()

            for update in self.usb_updates:
                if(selected_update == update.displayname):
                    self.display_text(selected_update+ "(USB-Update)\n")
                    if(update.type == "d"): readme_path = update.absolute_path+"/README.md"
                    elif(update.type == "t" or update.type == "z"): readme_path=update.extract_path+"/README.md"

                    (version, description) = get_software_details(readme_path)
                    if(version != "" and description != ""):
                        self.display_text(version)
                        self.display_text(description)
                    else:
                        self.display_text("(No description)")
            for update in self.git_updates:
                if(selected_update == update.name):
                    self.display_text(selected.text() + " (Server-Update):\n")
                    if(update.tag is not None):
                        self.display_text(update.tag.message)
                    else:
                        self.display_text("(No description)")

            self.DebugOutput.moveCursor(QtGui.QTextCursor.Start)
            self.DebugOutput.ensureCursorVisible()

    #   Update function called by clicking the Update/Rollback button
    #   Move the current touchscreen git project to another folder in root directory for backup
    #   Uses psutil to kill the current process, then calls sys.exit(0)
    def update(self):
        software = self.SoftwareList.currentRow()
        selected_version = self.SoftwareList.item(software, 0)
        if selected_version != None: #and selected_version.text() != self.app.applicationVersion(): #<--- Dont allow update to current version
            self.display_text("Updating....")
            self.backup_software()

            USB_update = False
            for update in self.usb_updates:
                if(selected_version.text() == update.displayname):
                    USB_update = True
                    ts_path = self.personality.gitrepopath
                    if(update.type == "d"):
                        shutil.rmtree(ts_path)
                        shutil.copytree(update.absolute_path, ts_path)
                    elif(update.type == "t" or update.type == "z"):
                        shutil.rmtree(ts_path)
                        shutil.copytree(update.extract_path, ts_path)
                    else:
                        self.display_text("Update failed. File type not supported")
            if(not USB_update): self.git.checkout(selected_version.text(), force=True)
            self.restart_program(sys.argv[0])
        else:
            self.display_text("Select a Version on list")
    
    def backup_software(self):
        #First check if the gitrepopath is valid
        ts_path = self.personality.gitrepopath
        backup_path = ts_path + "_backup"
        if(Path(ts_path).is_dir()):
            if(Path(backup_path).is_dir()):
                shutil.rmtree(backup_path)
            try:
                shutil.copytree(ts_path, backup_path)
            except Exception as e:
                print(e)

    def display_stored_text(self, text, replaceLastLine = False):
        if(replaceLastLine):
            self.store_text = self.store_text.strip()
            tmp = self.store_text.split("\n")
            tmp.pop()
            self.store_text = "\n".join(tmp)
            self.store_text += "\n"+ text + "\n"
            self.DebugOutput.clear()
            self.DebugOutput.append(self.store_text)
        else:
            self.store_text += text+ "\n"
            self.DebugOutput.clear()
            self.DebugOutput.append(self.store_text)

    def display_text(self, text, replaceLastLine=False):
        if(replaceLastLine):
            tmp = self.DebugOutput.textCursor()
            cursor = self.DebugOutput.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.select(QtGui.QTextCursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deletePreviousChar()
            self.DebugOutput.setTextCursor(tmp)
        self.DebugOutput.append(text)

    
    # Restart the program by using psutil. Grab the PID of the python application and kill it. 
    def restart_program(self, argument):

        # A quick hack: just exit and let the script restart
        # us. (Re-execing is a better long-term solution.)
        sys.exit(0)

        # try:
        #     p = psutil.Process(os.getpid())
        #     for handler in p.open_files() + p.connections():
        #         os.close(handler.fd)
        # except Exception as e:
        #     logging.error(e)

        # #Restart the program with the original arguments and python executable. 
        # python = sys.executable
        # os.execl(python, python, argument)
    
    def set_usb_mount_signals(self, tuple):
        (create_signal, delete_signal) = tuple
        create_signal.connect(self.update_usb_create)
        delete_signal.connect(self.update_usb_delete)
        
    def update_usb_create(self, mountpoint):
        print("UPDATE_USB_CREATE: path <%s>, actual path <%s>" % (mountpoint.path, mountpoint.actual_path))
        self.subdir = SubFileSystem(mountpoint.path)
        self.usb_mounted = True
        # print("USB create called");

    def update_usb_delete(self, path):
        self.usb_mounted = False
        # print("USB delete called")
        # self.usb_file_manager.clear_files()

    def set_usb_content_signal(self, signal):
        signal.connect(self.usb_content)
    def usb_content(self):
        print("USB CONTENT SIGNAL HERE")
    
    def check_usb_software(self):
        if(self.usb_mounted):
            self.usb_updates = self.subdir.list_ts_software_updates(self.unzip_progress)


    