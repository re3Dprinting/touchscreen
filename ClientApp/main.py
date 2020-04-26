#!/usr/bin/env python

#################################################################

import sys
import os
import glob
import logging
import getpass
import json
from pathlib import Path

from octo import setup_octoprint

from git import Repo, Git
from basewindow import BaseWindow

from touchscreen.touchdisplay import *
from touchscreen.util.personality import Personality
from touchscreen.fsutils.watchdogthread import WatchdogThread
from touchscreen.fsutils.mountfinder import MountFinder
from fsutils.mountpoint import MountPoint

from util.configid import get_touchscreen_commit_id
from util.log import setup_root_logger

from touchscreen.fsutils.ostype import *

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

#Load the config.properties file that should be located in the same location as Octoprint and touchscreen.
#A sample config.properties file is located within the setup-files directory.
def _load_properties():
    properties = {"name": "", 
                "motherboard" : "", 
                "wifissd" : "",
                "wifipassword" : "",
                "mode" : ""
                }

    #Grab the current directory were the git repository is initialized.
    tmp_path = Path(__file__).parent.absolute()
    current_path = Path(os.path.realpath(tmp_path)).parent

    #Move up one directory to grab the config.properties file
    config_path = current_path.parent.__str__() + "/config.properties"
    if(Path(config_path).is_file()):
        with open(config_path) as config_in:
            properties = json.load(config_in)
    else:
        _log("Please create a config.properties file within the same directory as Octoprint and Touchscreen!")

    #Grab the version from the current git repository. 
    #Will have to be adjusted if the user is updating software locally!!!!
    try:
        repo = Repo(current_path.__str__())
        properties["version"] = repo.active_branch.name
    except TypeError as e:
        print(e)
        properties["version"] = repo.git.describe()
    except Exception as e:
        print(e)
        properties["version"] = "Local"
        
    return properties

# This function takes care of all the high-level application
# initialization and setup. It is called belowe.
def main():

    # Setup logging first of all
    setup_root_logger()
    setup_local_logger(__name__)

    # We want to build a string to be displayed on the touchscreen
    # main screen that has helpful information for diagnestic
    # purposes. The string will consist of the application version,
    # our IP address, and some Git information.

    # Get the application version
    properties = _load_properties()
    version_string = properties["version"]

    # Get the IP address.
    ip_addr = get_ip()

    # Get the Git information. This will be the ID of the HEAD commit
    # plus indicators of whether any file has been changed, or if
    # GIT-unknown files are present.
    # Breaks in Python3.6
    config_id = get_touchscreen_commit_id()
    # config_id = "temp"

    # Now, the ID string is essentially just the concatenation of
    # these three bits of information.
    id_string = 'v' + version_string + ", IP: %s, Config ID: %s" % (ip_addr, config_id)

    # Print a banner to stdout.
    print("******************************************************************************")
    print("re:3D touchscreen starting. " + id_string)
    print("******************************************************************************")

    # And log the same banner.
    _log("******************************************************************************")
    _log("* re:3D touchscreen starting. " + id_string)
    _log("******************************************************************************")

    # The 'personality' mechanism is a way of specifying things that
    # will change from one OS to another. We create the personality
    # based on whether we're running Linux (including Raspbian) or
    # macOS.

    # # Get the platform name.
    # plat = sys.platform

    # if plat.startswith("linux"):
    if os_is_linux():

        # Linux
        # persona = Personality(True, "/media/usb0", "/home/pi/gcode-cache", "/home/pi/log-cache")
        persona = Personality(True, "/usb", "/home/pi/gcode-cache", "/home/pi/log-cache")

    # elif plat.startswith("darwin"):
    elif os_is_macos():
        # macOS
        if getpass.getuser() == "jct":
            octopath = "/Users/jct/Dropbox/re3D/touchscreen/OctoPrint"
            persona = Personality(False, "/Volumes", octopath + "/localgcode",
                                  octopath + "/log-cache")
        if getpass.getuser() == "npan":
            octopath = "/Users/npan/re3D/OctoPrint"
            persona = Personality(False, "/Volumes", octopath + "/localgcode",
                                  octopath + "/log-cache") 
                                  

    else:
        print("Unable to determine operating system, aborting...")
        persona = None
        sys.exit(1)

    #Personality object for Ubuntu
    # Please put this into the 'linux' section above.
    # persona = Personality(False, "/media/plloppii", "/home/plloppii/devel/gcode-cache", "/home/plloppii/devel/log-cache")
            
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
    display = TouchDisplay(printer_if, persona)
    display.SoftwareVersion.setText(id_string)

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
            display.print_pop.update_usb_create(current_mountpoint)

    # Set up the watchdog thread that watches the filesystem for
    # mounts of USB drives.
    wd_thread = WatchdogThread(display.print_pop, persona.watchpoint,
                               current_path, persona.localpath)

    # Set up the signals that let us safely communicate between
    # threads that watch the filesystem and the UI.
    usb_signal_tup = wd_thread.get_usb_signals()
    display.print_pop.set_usb_mount_signals(usb_signal_tup)
    
    usb_content_signal = wd_thread.get_usb_content_signal()
    display.print_pop.set_usb_content_signal(usb_content_signal)

    local_content_signal = wd_thread.get_local_content_signal()
    display.print_pop.set_local_content_signal(local_content_signal)

    # The print screen needs a reference to the local storage manager
    # so it can copy files from the USB into local storage.
    display.print_pop.set_storage_manager(local_storage_manager)

    # Show the top-level UI display...
    display.show()

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
