#!/usr/bin/env python

#################################################################

import sys
import os
import glob
import logging
import getpass
import json
from pathlib import Path
from shutil import copyfile

from PyQt5 import QtWidgets
from git import Repo, Git

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

def setup_local_logger(name):
    global logger
    logger = logging.getLogger(name)

def _log(message):
    global logger

    # NOTE: All messages logged here are at INFO level. Elsewhere,
    # always use DEBUG
    logger.info(message)


#Load the properties from the json file, config.properties
#   -config.properties acts as a static file that all windows can access
#   -the permission is set if the specified. 
#   -if the config.properties file is not found, create it in the correct directory.
def _load_properties(permission = "Default"):
    properties = {"name": "", 
                "motherboard" : "", 
                "wifissd" : "",
                "wifipassword" : "",
                "permission" : ""
                }
    #Grab the current directory were the git repository is initialized.
    tmp_path = Path(__file__).parent.absolute()
    current_path = Path(os.path.realpath(tmp_path)).parent

    #Move up one directory to grab the config.properties file
    config_path = current_path.parent.__str__() + "/config.properties"
    example_config_path = Path(os.path.realpath(tmp_path)).__str__() + "/setup-files/config.properties"
    
    #If the file does not exist, move the file over to the correct directory. 
    if( not Path(config_path).is_file() and Path(example_config_path).is_file() ):
        copyfile(example_config_path, config_path)

    #Catch exception if config_path still does not exist. 
    with open(config_path, "r+") as config_in:
        loaded_properties = json.load(config_in)
        properties = {**properties, **loaded_properties}
        #Set the permission if specified. Otherwise, keep as default.
        if not permission == "Default" and "permission" in properties: 
            properties["permission"] = permission
            config_in.seek(0)
            json.dump(properties, config_in, indent=4)
            config_in.truncate()

    #Grab the version from the current git repository. 
    #Will have to be adjusted if the user is updating software locally!!!!
    try:
        repo = Repo(current_path.__str__())
        current_version = next((tag for tag in repo.tags if tag.commit == repo.head.commit), None)
        properties["version"] = current_version.name
    #If no tag found, check for current branch
    except AttributeError as e:
        properties["version"] = repo.active_branch.name
    #If no branch/repo found, default to local. 
    except Exception as e:
        properties["version"] = "Local"
        
    return properties

# This function takes care of all the high-level application
# initialization and setup. It is called belowe.
def main():

    # Setup logging first of all
    setup_root_logger()
    setup_local_logger(__name__)

    # The 'personality' mechanism is a way of specifying things that
    # will change from one OS to another. We create the personality
    # based on whether we're running Linux (including Raspbian) or
    # macOS.
    if os_is_linux():
        # Linux
        persona = Personality(True, "/usb", "/home/pi/gcode-cache", "/home/pi/log-cache")
        properties = _load_properties()
    elif os_is_macos():
        # macOS
        if getpass.getuser() == "jct":
            octopath = "/Users/jct/Dropbox/re3D/touchscreen/OctoPrint"
            persona = Personality(False, "/Volumes", octopath + "/localgcode", octopath + "/log-cache")
            properties = _load_properties("developer")
        if getpass.getuser() == "npan":
            octopath = "/Users/npan/re3D/OctoPrint"
            persona = Personality(False, "/Volumes", octopath + "/localgcode", octopath + "/log-cache") 
            properties = _load_properties("developer")
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
    (printer, local_storage_manager) = setup_octoprint(persona)

    # Create a Printer Interface object. All our interactions with the
    # printer go through this object.
    printer_if = PrinterIF(printer)

    # Create the PyQt application
    app = QtWidgets.QApplication(sys.argv)

    app.setApplicationName(properties["name"])
    app.setApplicationVersion(version_string)

    # Create the top-level UI screen.
    mainwindow = MainWindow(printer_if, persona, properties)

    # mainwindow = Home(printer_if, persona)
    #mainwindow.SoftwareVersion.setText(id_string)

    # Check to see whether any USB filesystems are currently mounted.
    current_path = ""
    # possible_usb_mounts = MountFinder.thumbdrive_candidates()
    possible_usb_mounts = glob.glob("/usb/*")

    logger.debug("persona watchpoint = <%s>", persona.watchpoint)
    
    # If the mount finder located any possible USB mountpoints...
    if len(possible_usb_mounts) > 0:

        # ...loop through the possible USB mount points
        for possible_path in possible_usb_mounts:
            logger.debug("Possible path: <%s>", possible_path)

            # Break the first time we find a USB drive mounted on the
            # mount point we're watching.
            if possible_path.startswith(persona.watchpoint):
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
    wd_thread = WatchdogThread(print_page, persona.watchpoint,
                               current_path, persona.localpath)

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

def exception_hook(exctype, value, traceback):
    global logger
    logger.exception("**** Logging an uncaught exception", exc_info=(exctype, value, traceback))
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Hook up our exception handler
sys._excepthook = sys.excepthook
sys.excepthook = exception_hook

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
    main()
