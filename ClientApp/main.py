#!/usr/bin/env python

#################################################################

import sys
import os
import glob
import logging
import getpass
from pathlib import Path

from PyQt5 import QtWidgets

from octo import setup_octoprint
from touchscreen.mainwindow import MainWindow
from touchscreen.util.personality import Personality
from touchscreen.fsutils.watchdogthread import WatchdogThread
from touchscreen.fsutils.mountfinder import MountFinder
from fsutils.mountpoint import MountPoint

from util.configid import get_touchscreen_commit_id
from util.log import setup_root_logger

from touchscreen.fsutils.ostype import *
from constants import *

#################################################################

from printer_if import PrinterIF
from util.ip import get_ip
from util.load_properties import get_properties
from util.restore_backup import restore_backup

def setup_local_logger(name):
    global logger
    logger = logging.getLogger(name)

def _log(message):
    global logger

    # NOTE: All messages logged here are at INFO level. Elsewhere,
    # always use DEBUG
    logger.info(message)


# This function takes care of all the high-level application
# initialization and setup. It is called belowe.
class MainHandler():
    def __init__(self):
        # Hook up our exception handler
        sys._excepthook = sys.excepthook
        sys.excepthook = self.exception_hook

        # Setup logging first of all
        setup_root_logger()
        setup_local_logger(__name__)

        #Locate to the absolute path of the current path. Locate the root re3d dir where Octoprint, config.properties, and touchscreen folders lie.
        #     .
        # ├── OctoPrint 
        # ├── config.properties
        # └── touchscreen 
        tmp_path = Path(__file__).parent.absolute() #Path of the symbolic link
        touchscreen_path = Path(os.path.realpath(tmp_path)) #Grab absolute path from symbolic link, Location of the main.py file (ClientApp directory)

        # The 'personality' mechanism is a way of specifying things that
        # will change from one OS to another. We create the personality
        # based on whether we're running Linux (including Raspbian) or
        # macOS.
        if os_is_linux():
            # Linux
            self.persona = Personality(True, "/usb", "/home/pi/gcode-cache", "/home/pi/log-cache", touchscreen_path)
            properties = get_properties(self.persona)
        elif os_is_macos():
            # macOS
            if getpass.getuser() == "jct":
                octopath = "/Users/jct/Dropbox/re3D/touchscreen/OctoPrint"
                self.persona = Personality(False, "/Volumes", octopath + "/localgcode", octopath + "/log-cache", touchscreen_path)
                properties = get_properties(self.persona, "developer")
            if getpass.getuser() == "npan":
                octopath = "/Users/npan/re3D/OctoPrint"
                self.persona = Personality(False, "/Volumes", octopath + "/localgcode", octopath + "/log-cache", touchscreen_path) 
                properties = get_properties(self.persona, "developer")
        else:
            print("Unable to determine operating system, aborting...")
            sys.exit(1)
        

        # We want to build a string to be displayed on the touchscreen
        # main screen that has helpful information for diagnestic
        # purposes. The string will consist of the application version,
        # our IP address, and some Git information.

        # Get the application version
        version_string = properties["version"]

        # Get the IP address.
        ip_addr = get_ip()
        ip_string = "IP: " + ip_addr

        # Get the Git information. This will be the ID of the HEAD commit
        # plus indicators of whether any file has been changed, or if
        # GIT-unknown files are present.
        # Breaks in Python3.6
        config_id = get_touchscreen_commit_id()
        config_string = "%s/%s" % (version_string, config_id)

        # Print a banner to stdout.
        print("******************************************************************************")
        print("re:3D touchscreen starting %s %s " % (ip_string, version_string))
        print("******************************************************************************")

        # And log the same banner.
        _log("******************************************************************************")
        _log("re:3D touchscreen starting %s %s " % (ip_string, version_string))
        _log("******************************************************************************")


        # Set up all the OctoPrint stuff. We need two bits of information
        # from that: the printer and the storage manager.
        (printer, local_storage_manager) = setup_octoprint(self.persona)

        # Create a Printer Interface object. All our interactions with the
        # printer go through this object.
        printer_if = PrinterIF(printer)

        # Create the PyQt application
        app = QtWidgets.QApplication(sys.argv)

        app.setApplicationName(properties["name"])
        app.setApplicationVersion(version_string)

        # Create the top-level UI screen.
        mainwindow = MainWindow(printer_if, self.persona, properties)

        # mainwindow = Home(printer_if, self.persona)
        #mainwindow.SoftwareVersion.setText(id_string)

        # Check to see whether any USB filesystems are currently mounted.
        current_path = ""
        # possible_usb_mounts = MountFinder.thumbdrive_candidates()
        possible_usb_mounts = glob.glob("/usb/*")

        logger.debug("persona watchpoint = <%s>", self.persona.watchpoint)
        
        # If the mount finder located any possible USB mountpoints...
        if len(possible_usb_mounts) > 0:

            # ...loop through the possible USB mount points
            for possible_path in possible_usb_mounts:
                logger.debug("Possible path: <%s>", possible_path)

                # Break the first time we find a USB drive mounted on the
                # mount point we're watching.
                if possible_path.startswith(self.persona.watchpoint):
                    current_path = possible_path
                    break

            if current_path != "":
                logger.debug("Initial USB path = <%s>" % current_path)
                
                # There seems to be a thumb drive plugged in. Tell the UI
                # print window to use it as the inital file list.
                current_mountpoint = MountPoint(current_path)
                print_page = mainwindow.get_page(k_print_page)
                print_page.update_usb_create(current_mountpoint)

        # Set up the watchdog thread that watches the filesystem for
        # mounts of USB drives.
        print_page = mainwindow.get_page(k_print_page)
        wd_thread = WatchdogThread(print_page, self.persona.watchpoint,
                                current_path, self.persona.localpath)

        # Set up the signals that let us safely communicate between
        # threads that watch the filesystem and the UI.
        usb_signal_tup = wd_thread.get_usb_signals()
        print_page.set_usb_mount_signals(usb_signal_tup)
        
        usb_content_signal = wd_thread.get_usb_content_signal()
        print_page.set_usb_content_signal(usb_content_signal)

        local_content_signal = wd_thread.get_local_content_signal()
        print_page.set_local_content_signal(local_content_signal)

        # The print screen needs a reference to the local storage manager
        # so it can copy files from the USB into local storage.
        print_page.set_storage_manager(local_storage_manager)

        mainwindow.set_left_status(ip_string)
        mainwindow.set_middle_status("Printer: Offline")
        mainwindow.set_right_status(config_string)

        # Show the top-level UI display...
        mainwindow.show()

        # ...and kick off the UI event loop. This function does not
        # return.
        app.exec_()

    # Define an exception hook to log exceptions that would normally be
    # caught and handled by PyQt5. We do our own handling to ensure that
    # the stack trace goes into the log.

    def exception_hook(self, exctype, value, traceback):
        global logger
        logger.exception("**** Logging an uncaught exception", exc_info=(exctype, value, traceback))
        sys._excepthook(exctype, value, traceback)

        #Restore backup version if backup exists. Backup is created, when a update is clicked. 
        restore_backup(self.persona)
        sys.exit(1)



from datetime import datetime
from time import sleep

# def dummyall():
#     logger = setup_root_logger()

#     while True:
#         # Build up a string to represent the tarball filename, starting with the date.
#         now = datetime.now()
#         nowstr = now.strftime("%Y-%m-%d-%H-%M-%S.%f")
#         # for i in range(1, 1000000):
#         logger.info("*****************************%s*********************************" % nowstr)

# Everything's now defined. All we have to do is call it.
if __name__ == "__main__":
    # dummyall()
    MainHandler()
