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
from PyQt5 import QtCore, QtGui, QtWidgets, QtQuickWidgets, QtQuick
from PyQt5.QtQml import QQmlEngine, qmlRegisterType

from fsutils.subfilesystem import SubFileSystem

import git
from enum import Enum

import zipfile
import tarfile
from threading import Thread
from qt.userupdatepage_qt import Ui_UserUpdatePage
from notification import Notification
from basepage import BasePage
from util.load_properties import get_software_details
from model.tablemodel import TableModel


class UpdateType(Enum):
    USB = 1
    GIT = 2
class UpdateObject():
    def __init__(self, softwaretype, softwareupdate):
        self.type = softwaretype
        self.obj = softwareupdate
        if self.type == UpdateType.USB:
            self.name = softwareupdate.displayname
            self.date = softwareupdate.timestamp
        elif self.type == UpdateType.GIT:
            self.name = softwareupdate.name
            self.date = time.strftime('%I:%M%p %m/%d/%y', time.localtime(softwareupdate.commit.committed_date))
    def getDataFromIndex(self, index):
        if(index == 0): return self.name
        elif(index == 1): return self.date
        return None

class UserUpdatePage(BasePage, Ui_UserUpdatePage):
    # Signal sent to notify ui is ready to be updated.
    uiUpdateSignal = pyqtSignal(str)
    unzipProgressSignal = pyqtSignal(str, bool)
    rowClickedSignal = pyqtSignal(int)
    def __init__(self, context):
        super(UserUpdatePage, self).__init__()

        self._logger = logging.getLogger(__name__)
        self._log("UserUpdate __init__")
        self.setupUi(self)

        self.personality = context.personality
        self.ui_controller = context.ui_controller
        self.properties = context.properties

        self.app = QtWidgets.QApplication.instance()
        self.new_version_avalible = False
        # self.debug = (self.properties["debug"] == "true")
        self.debug = True

        # Subdirectory object to check for USB software updates.
        self.subdir = SubFileSystem(self.personality.watchpoint)
        self.usb_mounted = False

        # Get the current path (local repository) and make sure that the github link is the current repository.
        try:
            self.repo = git.Repo(self.personality.gitrepopath)
            self.git = git.Git(self.personality.gitrepopath)
            found_remote = False
            # Check if re3d remote repository is in current remote tree
            for r in self.repo.remotes:
                if r.name == "re3d":
                    self.remote_repo = r
                    found_remote = True
            # If re3d repo does not exist, add it as a remote.
            if not found_remote:
                self.remote_repo = self.repo.create_remote(
                    "re3d", "https://github.com/re3Dprinting/touchscreen")
        except Exception as e:
            print("userupdate: __init__() exception: ", e)

        self.update_Thread = None
        # Initialize the array for Git Software Updates and USB Software Updates
        self.usb_updates = []
        self.all_found_updates = []

        # Signal to notify that UI updates are ready from a thread
        self.uiUpdateSignal.connect(self.ui_update_list)
        # Signal passed to subfilesystem to update unzipping progress in UI
        self.unzipProgressSignal.connect(self.display_stored_text)
        self.store_text = ""

        self.DebugOutput.setLineWrapMode(QtWidgets.QTextBrowser.NoWrap)

        #  Append the version to the current version window.
        temp = self.CurrentVersion.text() + " " + self.app.applicationVersion()
        self.CurrentVersion.setText(temp)

        self.setStyleProperty(self.BottomBar, "bottom-bar")
        self.setStyleProperty(self.LeftBar, "left-bar")
        self.setAllTransparentButton(
            [self.Back, self.Update, self.CheckUpdate], True)
        self.setStyleProperty(self.CurrentVersion,
                              "white-transparent-text font-m align-center")

        self.SoftwareTable = QtQuickWidgets.QQuickWidget(self.MainLayout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SoftwareTable.sizePolicy().hasHeightForWidth())
        self.SoftwareTable.setSizePolicy(sizePolicy)
        self.SoftwareTable.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        self.softwareTableModel = TableModel(self, self.rowClickedSignal)
        self.rowClickedSignal.connect(self.show_update_message)
        self.SoftwareTable.rootContext().setContextProperty("tableModel", self.softwareTableModel)
        self.selectedRow = None

        self.SoftwareTable.setSource(QtCore.QUrl("qrc:/qml/table.qml"))
        self.SoftwareTable.setObjectName("SoftwareTable")
        self.SoftwareTableLayout.addWidget(self.SoftwareTable)


        # # OLD IMPLEMENTATION OF QT WIDGET, QTABLEWIDGET. DID NOT WORK WITH KINETIC SCROLLING ON TOUCHSCREEN.
        # # Make the selection Behavior as selecting the entire row
        # self.SoftwareList.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        # self.SoftwareList.setSelectionMode(
        #     QtWidgets.QTableView.SingleSelection)
        # # Update the side dialog box when a software version is selected.
        # self.SoftwareList.itemSelectionChanged.connect(
        #     self.show_update_message)
        # # Hide the vertical header which contains the Index of the row.
        # self.SoftwareList.verticalHeader().hide()
        # # Stretch out the horizontal header to take up the entire view
        # header = self.SoftwareList.horizontalHeader()
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # self.SoftwareList.setVerticalScrollMode(
        #     QtWidgets.QAbstractItemView.ScrollPerPixel)
        # self.SoftwareList.setAutoScroll(False)
        # QtWidgets.QScroller.grabGesture(
        #     self.SoftwareList, QtWidgets.QScroller.LeftMouseButtonGesture)

        self.Back.clicked.connect(self.back)
        self.CheckUpdate.clicked.connect(self.checkupdate)
        self.Update.clicked.connect(self.update)

        

    def checkupdate(self):
        self.DebugOutput.clear()
        self.store_text = ""

        self.usb_updates = []
        self.all_found_updates = []
        self.display_stored_text("Fetching Server Updates...")

        self.update_Thread = Thread(target=self.checkupdate_handler)
        self.update_Thread.setDaemon(True)
        self.update_Thread.start()

    def checkupdate_handler(self):
        """
        Handler that is ran on a seperate thread, that checks the Git software updates first if Wifi is enabled
        Pushes the updates up to the UI if ready, then checks for USB updates.
        Then pushes updates to the UI a second time.
        """
        try:
            self.uiUpdateSignal.emit("STARTING-FETCH")
            if(self.properties["wifienabled"]):
                self.check_git_software()
                self.uiUpdateSignal.emit("Server Updates found... \nFetching USB Updates...")
            usbUpdatesFound = self.check_usb_software()
            if(usbUpdatesFound):
                self.uiUpdateSignal.emit("USB Updates found.")
            else:
                self.uiUpdateSignal.emit("No USB Updates Found.")
            self.uiUpdateSignal.emit("FINISHED-FETCH")
        except Exception as e:
            err = "An Error has occured: \n" + str(type(e)) + "\n"+str(e)
            self.display_text(err)
            print("userupdate: checkupdate() exception: ", type(e), e)

    def ui_update_list(self, msg):
        if(msg == "STARTING-FETCH"):
            self.CheckUpdate.setEnabled(False)
            return
        if(msg == "FINISHED-FETCH"):
            self.CheckUpdate.setEnabled(True)
            return

        self.display_stored_text(msg)

        self.softwareTableModel.updateData(self.all_found_updates)
        self.softwareTableModel.layoutChanged.emit()

        # If no versions are found, push a debug message to the window.
        # If there is a newer version avalible, create a notification object and return it to be caught by the window.
        if(len(self.all_found_updates) == 0):
            self.display_text("No software versions found on server or on USB")
        if(self.new_version_avalible):
            return Notification("A new software version is available!\nTo update, go to Settings > Software Update")

    def check_git_software(self):
        # Delete tags if they contain "release/"
        for tag in self.repo.tags:
            if("release/" in tag.name or
                "devel/" in tag.name or
                    "hotfix/" in tag.name):
                try:
                    self.repo.delete_tag(tag)
                except:
                    pass
        try:
            self.remote_repo.fetch("-tf")
        except git.GitCommandError as e:
            if("reference broken" in e.stderr):
                shutil.rmtree(self.personality.gitrepopath+"/.git/refs/tags")

        self.remote_repo.fetch("-tf")

        tags = sorted(self.repo.tags, key=lambda t: t.commit.committed_date)
        tags.reverse()

        # Grab the current version and check if it is a beta version.
        current_v = self.app.applicationVersion()
        curr_isCustomerRelease = self.isCustomerRelease(current_v)

        # Check each tag and if it is a "release" tag.
        # Append the tag to the list on the table widget.
        for t in tags:
            # Grab the current Version and the given version and see if they are beta versions.
            given_v = t.name
            given_isCustomerRelease = self.isCustomerRelease(given_v)

            # Skip over all tags that contain archive
            if("archive" in t.name):
                continue

            if(("release" in t.name or
                "devel" in t.name or
                "hotfix" in t.name)
                    and (not self.properties["permission"] == "developer")):
                continue

            if("beta" in t.name and not(self.properties["permission"] == "developer" or self.properties["permission"] == "beta-tester")):
                continue

            # Filter out any remaining tags that are not in the given X.X.X format.
            if(self.properties["permission"] == "customer" and not given_isCustomerRelease):
                continue

            self.all_found_updates.append(UpdateObject(UpdateType.GIT, t))

            # Check for an update if and only if the current version and given version both follow the X.X.X sematic versioning.
            if(curr_isCustomerRelease and given_isCustomerRelease):
                # Check if there is a newer software version avalible.
                self.checkagainstcurrent(current_v, given_v)

    # Is Customer Release only if version is in format of X.X.X
    def isCustomerRelease(self, version):
        version = version.split(".")
        if(len(version) < 3):
            return False
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

    def show_update_message(self, row):
        """
        Callback when a item in the updates list is selected.
        Determines if it is a USB or Git update. Shows changelog from file(USB Update) or Git tag message
        """
        # item = self.SoftwareList.currentRow()
        # selected = self.SoftwareList.item(item, 0)
        self.selectedRow = row

        self.DebugOutput.clear()
        update = self.all_found_updates[row]

        if update.type == UpdateType.USB:
            self.display_text(update.name + "(USB-Update)\n")
            if( update.obj.type  == "d"):
                readme_path = update.obj.absolute_path+"/README.md"
            elif(update.obj.type == "t" or update.type == "z"):
                readme_path = update.obj.extract_path+"/README.md"
            (version, description) = get_software_details(readme_path)
            if(version != "" and description != ""):
                self.display_text(version)
                self.display_text(description)
            else:
                self.display_text("(No description)")
        elif update.type == UpdateType.GIT:
            self.display_text(update.name + " (Server-Update):\n")
            if(update.obj.tag is not None):
                self.display_text(update.obj.tag.message)
            else:
                self.display_text("(No description)")
            
        self.DebugOutput.moveCursor(QtGui.QTextCursor.Start)
        self.DebugOutput.ensureCursorVisible()

            
    #   Update function called by clicking the Update/Rollback button
    #   Move the current touchscreen git project to another folder in root directory for backup
    #   Uses psutil to kill the current process, then calls sys.exit(0)
    def update(self):
        if self.selectedRow != None:
            self.display_text("Updating....")
            self.backup_software()

            update = self.all_found_updates[self.selectedRow]
            if(update.type == UpdateType.USB):
                ts_path = self.personality.gitrepopath
                if(update.type == "d"):
                    shutil.rmtree(ts_path)
                    shutil.copytree(update.obj.absolute_path, ts_path)
                elif(update.type == "t" or update.type == "z"):
                    shutil.rmtree(ts_path)
                    shutil.copytree(update.obj.extract_path, ts_path)
                else:
                    self.display_text("Update failed. File type not supported")
            elif(update.type == UpdateType.GIT):
                self.git.checkout(update.name, force=True)

            sys.exit(0)
        else:
            self.display_text("Select a Version on list")
        

    def backup_software(self):
        # First check if the gitrepopath is valid
        ts_path = self.personality.gitrepopath
        backup_path = ts_path + "_backup"
        if(Path(ts_path).is_dir()):
            if(Path(backup_path).is_dir()):
                shutil.rmtree(backup_path)
            try:
                shutil.copytree(ts_path, backup_path)
            except Exception as e:
                print(e)

    def display_stored_text(self, text, replaceLastLine=False):
        if(replaceLastLine):
            self.store_text = self.store_text.strip()
            tmp = self.store_text.split("\n")
            tmp.pop()
            self.store_text = "\n".join(tmp)
            self.store_text += "\n" + text + "\n"
            self.DebugOutput.clear()
            self.DebugOutput.append(self.store_text)
        else:
            self.store_text += text + "\n"
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


    def set_usb_mount_signals(self, tuple):
        (create_signal, delete_signal) = tuple
        create_signal.connect(self.update_usb_create)
        delete_signal.connect(self.update_usb_delete)

    def update_usb_create(self, mountpoint):
        # print("UPDATE_USB_CREATE: path <%s>, actual path <%s>" % (mountpoint.path, mountpoint.actual_path))
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
        pass
        # print("USB CONTENT SIGNAL HERE")

    #Pass in the signal to show the progress of unzipping the zipped software file.
    def check_usb_software(self):
        if(self.usb_mounted):
            usbUpdates = self.subdir.list_ts_software_updates(self.unzipProgressSignal)
            for update in usbUpdates:
                self.all_found_updates.insert(0, UpdateObject(UpdateType.USB, update))
            if len(usbUpdates) > 0:
                return True
        return False
            