#!/usr/bin/env python

#################################################################

print("Doing OctoPrint imports...")

import logging

from octoprint import settings
from octoprint import printer
from octoprint import plugin
import octoprint.filemanager
from octoprint.printer.standard import Printer
from octoprint.printer.standard import PrinterCallback
from octoprint.printer import profile
import octoprint.events
from octoprint.filemanager import analysis
from octoprint import filemanager
from octoprint.filemanager import storage
from octoprint.events import GenericEventListener



#################################################################

print("Doing touchscreen imports...")

import time
import serial
import serial.tools.list_ports

from touchscreen.Client.g_serial import *
from touchscreen.Client.g_client import *
from touchscreen.Client.g_data import *

from touchscreen.touchdisplay import *
from touchscreen.personality import Personality
from touchscreen.fsutils.watchdogthread import WatchdogThread
from touchscreen.fsutils.mountfinder import MountFinder

import sys
import threading
import os

#################################################################

print("Doing local imports...")

from printer_if import PrinterIF

# Get the EventManager singleton
event_manager = octoprint.events.eventManager()

#################################################################
# Octoprint classes

class JTEventListener:
        def __init__(self):
            # print("Subscribing to lots of stuff(?)")
            GenericEventListener.__init__(self)

            # attr_names = filter(lambda x: not x.startswith("_"), dir(octoprint.events.Events))
            # for name in attr_names:
            #         attr = octoprint.events.Events.__dict__[name]
            #         if type(attr) is str:
            #                 # print("******** Got a string: <%s>" % (attr))
            #                 event_name = attr
            #                 event_manager.subscribe(event_name, self.jeventCallback)

            # levents = list(events)

            # print("Events:", events)
            # print("List events:", levents)

            # self.subscribe(events)
            # count = len(levents)
            # print("Subscribing to:", levents)
            # for event in levents:
            #     print("Subscribing to", event)
            #     event_manager.subscribe(event, self.jeventCallback)

            # event_manager.subscribe(octoprint.events.Events.STARTUP, self.jeventCallback)
            # event_manager.subscribe("PrinterStateChanged", self.jeventCallback)
            # event_manager.dumpListeners()

#         def jeventCallback(self, event, payload):
# #               GenericEventListener.eventCallback(self, event, payload)
#                 pre = "***"
#                 if event == "PositionUpdate":
#                         return
#                 if event == "PrinterStateChanged":
#                         pre = "######"

#                 print("%s Received event: %s (Payload: %r)" % (pre, event, payload))

class JTCallback(PrinterCallback):
    def on_printer_add_message(self, data):
        if data.startswith("T:") or data.startswith("X:"):
                return
        # print("Received callback message data:", data)
        pass

    # def on_printer_send_current_data(self, data):
    #     print("Received current data: <%s>" % (data))
        

### Main ###

if __name__ == "__main__":

    #################################################################
    # This is the octoprint area
    print("Setting up logging")
    logging.basicConfig(filename='jt.log', level=logging.DEBUG)

    # Initialize settings
    print("Initializing settings.")
    settings = octoprint.settings.settings(True)

    # Initialize plugin manager
    print("Initializing plugin manager")
    plugin.plugin_manager(True)

    # Initialize profile manager
    print("Creating profile manager")
    profile_manager = profile.PrinterProfileManager()

    # Create an analysis queue
    print("Creating analysis queue")
    analysis_queue = analysis.AnalysisQueue({})

    # Create the file manager
    print("Creating file manager")

    # persona = Personality(False, "/Volumes", "/Users/jct/localgcode")
    # persona = Personality(False, "/Volumes", "/Users/jct/Dropbox/re3D/touchscreen/octoprint/localgcode")
    persona = Personality(True, "/media/pi", "/home/pi/gcode-cache")

    storage_managers = dict()
    local_storage_manager = storage.LocalFileStorage(persona.localpath)
    storage_managers[octoprint.filemanager.FileDestinations.LOCAL] = local_storage_manager

#    foobar = DiskFileWrapper("foobar", "/Users/jct/Desktop/foobar.gcode", False)
#    local_storage_manager.add_file("foobar.gcode", foobar, allow_overwrite=True)
#    baz.select_file("foobar.gcode", False, True)

    file_manager = octoprint.filemanager.FileManager(analysis_queue, None, None, initial_storage_managers=storage_managers)

    # debug_event_listener = DebugEventListener()
    jt_callback = JTCallback()

    printer = Printer(file_manager, analysis_queue, profile_manager)
    printer.register_callback(jt_callback)

    event_listener = JTEventListener()

    printer_if = PrinterIF(printer)

    #################################################################
    # This is the touchscreen area

    print("Doing touchscreen stuff")

    print("Starting the data thread")
    data_thread = g_data()
    client_conn = g_client(data_thread)
    serial_conn = g_serial(data_thread)
    data_thread.start()

    print("Creating the UI")
    app = QtWidgets.QApplication(sys.argv)

    display = TouchDisplay(client_conn, printer_if, persona)
    display.show()

    print("Starting the events flow")
    event_manager.fire(octoprint.events.Events.STARTUP)

    print("Figuring out whether a USB drive is plugged in")
    possible_usb_mounts = MountFinder.thumbdrive_candidates()

    current_path = ""

    if len(possible_usb_mounts) > 0:
        # There seems to be a thumb drive plugged in. Tell the UI
        # print window to use it as the inital file list.
            current_path = ""
            for possible_path in possible_usb_mounts:
                if possible_path.startswith(persona.watchpoint):
                    current_path = possible_path
                    break
            if current_path != "":
                    print("current_path: <%s>" % current_path)
                    print("Current path (possible?) = <%s>" % current_path)
                    display.print_pop.update_usb_create(current_path)

    print("Creating the watchdog thread")
    wd_thread = WatchdogThread(display.print_pop, persona.watchpoint,
                               current_path, persona.localpath)

    usb_signal_tup = wd_thread.get_usb_signals()
    display.print_pop.set_usb_mount_signals(usb_signal_tup)

    usb_content_signal = wd_thread.get_usb_content_signal()
    display.print_pop.set_usb_content_signal(usb_content_signal)

    local_content_signal = wd_thread.get_local_content_signal()
    display.print_pop.set_local_content_signal(local_content_signal)

    display.print_pop.set_storage_manager(local_storage_manager)

    print("Connecting the printer (DEBUG USE ONLY)")
    printer.connect("/dev/tty.usbserial-DN02B57Q", 250000)
    # printer.connect("/dev/tty.usbserial-143320", 115200)

    print("Starting the interpreter thread")
    
    
    print("Starting the UI")
    app.exec_()
