#!/usr/bin/python3.4

from builtins import str
import os
import psutil
import shutil
from pathlib import Path
import time
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets

from .fsutils.subfilesystem import SubFileSystem

from git import Repo
from git import Git

import zipfile, tarfile
from qt.userupdatepage_qt import Ui_UserUpdatePage
from notification import Notification
from basepage import BasePage
from basewindow import BaseWindow


class UserUpdatePage(BasePage, Ui_UserUpdatePage, BaseWindow):
    #Signal sent to notify a USB device was plugged in.
    update_signal = pyqtSignal(str)

    def __init__(self, context):
        super(UserUpdatePage, self).__init__()
        self.base_init()

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
        
        #Get the current path (local repository) and make sure that the github link is the current repository.
        try:
            self.git = Git(self.personality.gitrepopath)
            self.repo = Repo(self.personality.gitrepopath)
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
        except Exception as e:
            print("userupdate: __init__() exception: ", e)
            
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

        self.checkupdate()

    def checkupdate(self):
        #Fetch all of the tags from the remote repository.
        try:
            #Delete tags if they contain "release/"
            for tag in self.repo.tags:
                if("release/" in tag.name or 
                    "devel/" in tag.name or 
                    "hotfix/" in tag.name):
                    self.repo.delete_tag(tag)

            self.remote_repo.fetch("-tf")
            tags = sorted(self.repo.tags, key=lambda t: t.commit.committed_date)
            tags.reverse()

            self.SoftwareList.setRowCount(0)

            #Grab the current version and check if it is a beta version. 
            current_v = self.app.applicationVersion()
            curr_isCustomerRelease = self.isCustomerRelease(current_v)

            # Check each tag and if it is a "release" tag. 
            # Append the tag to the list on the table widget. 
            self.current_tags = []
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

                self.current_tags.append(t)
                tag_date = time.strftime('%I:%M%p %m/%d/%y', time.localtime(t.commit.committed_date))

                #Check for an update if and only if the current version and given version both follow the X.X.X sematic versioning. 
                if(curr_isCustomerRelease and given_isCustomerRelease):
                    #Check if there is a newer software version avalible. 
                    self.checkagainstcurrent(current_v, given_v)
                
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
            if(self.SoftwareList.rowCount() == 0): self.print_debug("No software versions found. The server might be down, please try again later.")
            elif(self.new_version_avalible):
                return Notification("A new software version is available!\nTo update, go to Settings > Software Update")
        except Exception as e:
            print("userupdate: checkupdate() exception: ", e)

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

    #Grab the tag message and display it. 
    def show_tag_message(self):
        item = self.SoftwareList.currentRow()
        selected = self.SoftwareList.item(item, 0)
        if(selected != None):
            self.DebugOutput.clear()
            self.print_debug(selected.text() + " changelog:\n")
            version = selected.text()
            for tag in self.current_tags:
                if(version == tag.name):
                    if tag.tag is None:
                        self.print_debug("(No description)")
                    else:
                        self.print_debug(tag.tag.message)
            self.DebugOutput.moveCursor(QtGui.QTextCursor.Start)
            self.DebugOutput.ensureCursorVisible()

    #   Update function called by clicking the Update/Rollback button
    #   Move the current touchscreen git project to another folder in root directory for backup
    #   Uses psutil to kill the current process, then calls sys.exit(0)
    def update(self):
        software = self.SoftwareList.currentRow()
        selected_version = self.SoftwareList.item(software, 0)
        if selected_version != None: #and selected_version.text() != self.app.applicationVersion(): #<--- Dont allow update to current version
            self.print_debug("Updating....")
            self.backup_software()

            self.git.checkout(selected_version.text())
            if(self.personality.fullscreen == False): self.restart_program(sys.argv[0])
            else: self.restart_program(sys.argv[0])
        else:
            self.print_debug("Select a Version on list")
    
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



    def print_debug(self, text):
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
        self.check_usb_software()

    def update_usb_delete(self, path):
        pass
        # self.usb_file_manager.clear_files()


    def set_usb_content_signal(self, signal):
        signal.connect(self.check_usb_software)
    def check_usb_software(self):
        usb_updates = self.subdir.list_ts_software_updates()
        # for update in usb_updates:
        #     update.dump()

        
        #     print(file.displayname, " ", file.type)
        #     if file.type == 'd':
        #         print(file.displayname)
        
        #Validate that the directory, zip, or tar.gz is a valid touchscreen software 
        #Compare the checksum with the checksum within the touchscreen software directory

        #Update Software list with local files listed first.

        #If clicked update, copy the software onto the local directory, d
    