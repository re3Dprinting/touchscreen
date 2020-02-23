#!/usr/bin/env python

#################################################################

import logging

import sys
import threading
import os

import time
import serial
import serial.tools.list_ports

from pathlib import Path
from octo import setup_octoprint

from touchscreen.Client.g_serial import *
from touchscreen.Client.g_client import *
from touchscreen.Client.g_data import *

from touchscreen.touchdisplay import *
from touchscreen.util.personality import Personality
from touchscreen.fsutils.watchdogthread import WatchdogThread
from touchscreen.fsutils.mountfinder import MountFinder

from util.configid import get_touchscreen_commit_id
from util.log import setup_root_logger

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


if __name__ == "__main__":

    # Setup logging first of all

    setup_root_logger()
    setup_local_logger(__name__)

    # The first log entry will be the config ID.
    config_id = get_touchscreen_commit_id()


    ip_addr = get_ip()

    id_string = "IP: %s, Config ID: %s" % (ip_addr, config_id)
    
    print("******************************************************************************")
    print("re:3D touchscreen starting. " + id_string)
    print("******************************************************************************")

    _log("******************************************************************************")
    _log("* re:3D touchscreen starting. " + id_string)
    _log("******************************************************************************")

    # Set up the personality based on OS type.
    plat = sys.platform

    if plat.startswith("linux"):
        # Linux
        persona = Personality(True, "/media/pi", "/home/pi/gcode-cache")
        # persona = Personality(True, "/media", "/home/pi/gcode-cache")

    elif plat.startswith("darwin"):
        # macOS
        persona = Personality(False, "/Volumes", "/Users/jct/Dropbox/re3D/touchscreen/OctoPrint-1.4.0rc3/localgcode")

    else:
        print("Unable to determine operating system, aborting...")
        persona = None
        sys.exit(1)
            
    # Set up all the OctoPrint stuff. We need two bits of information
    # from that: the printer and the storage manager.
    (printer, local_storage_manager) = setup_octoprint(persona)

    printer_if = PrinterIF(printer)

    # Can we get rid of these now?
    data_thread = g_data()
    client_conn = g_client(data_thread)
    serial_conn = g_serial(data_thread)
    data_thread.start()

    app = QtWidgets.QApplication(sys.argv)

    properties = {}
    config_path = Path(__file__).parent.absolute().__str__() + "/config.properties"
    for line in open(config_path):
        properties[line.split("=")[0]] = line.split("=")[1].strip()

    version_string = properties["version"]

    app.setApplicationName(properties["name"])
    app.setApplicationVersion(version_string)

    id_string = 'v' + version_string + ", " + id_string

    # Create the top-level UI screen.
    display = TouchDisplay(client_conn, printer_if, persona)
    display.SoftwareVersion.setText(id_string)

    # Check to see whether any USB filesystems are currently mounted.
    current_path = ""
    possible_usb_mounts = MountFinder.thumbdrive_candidates()

    # If the mount finder located any possible USB mountpoints...
    if len(possible_usb_mounts) > 0:

        # ...loop through the possible USB mount points
        for possible_path in possible_usb_mounts:

            # Break the first time we find a USB drive mounted on the
            # mount point we're watching.
            if possible_path.startswith(persona.watchpoint):
                current_path = possible_path
                break

        if current_path != "":
            # There seems to be a thumb drive plugged in. Tell the UI
            # print window to use it as the inital file list.
            display.print_pop.update_usb_create(current_path)

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
