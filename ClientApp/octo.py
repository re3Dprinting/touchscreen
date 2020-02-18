#!/usr/bin/env python

#################################################################

import logging
from logging.handlers import RotatingFileHandler

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

import sys
import threading
import os

import time
import serial
import serial.tools.list_ports
from pathlib import Path

from touchscreen.Client.g_serial import *
from touchscreen.Client.g_client import *
from touchscreen.Client.g_data import *

from touchscreen.touchdisplay import *
from touchscreen.util.personality import Personality
from touchscreen.fsutils.watchdogthread import WatchdogThread
from touchscreen.fsutils.mountfinder import MountFinder

from touchscreen.gigabot_profile import gigabot_profile
from util.configid import get_touchscreen_commit_id

#################################################################

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
        
from octoprint.printer.profile import BedFormFactor
from octoprint.printer.profile import BedOrigin

gigabot_profile = dict(
		id = "_gigabot",
		name = "Gigabot",
		model = "re:3D Gigabot",
		color = "default",
		volume=dict(
			width = 600,
			depth = 600,
			height = 600,
			formFactor = BedFormFactor.RECTANGULAR,
			origin = BedOrigin.LOWERLEFT,
			custom_box = False
		),
		heatedBed = True,
		heatedChamber = False,
		extruder=dict(
			count = 2,
			offsets = [
			    (0, 0),
                            (0, 0)
			],
			nozzleDiameter = 0.4,
			sharedNozzle = False
		),
		axes=dict(
			x = dict(speed=6000, inverted=False),
			y = dict(speed=6000, inverted=False),
			z = dict(speed=200, inverted=False),
			e = dict(speed=300, inverted=False)
		)
	)

def setup_local_logger(name):
    global logger
    logger = logging.getLogger(name)

def _log(message):
    global logger
    # NOTE: All messages logged here are at INFO level. Elsewhere,
    # always use DEBUG
    logger.info(message)

def dump_logger_hierarchy(note, log_to_debug):
    print(note, ": Dumping logger", log_to_debug)
    while log_to_debug is not None:
	    print("*** level: %s, name: %s, handlers: %s" % (log_to_debug.level,
							     log_to_debug.name,
							     log_to_debug.handlers))
	    log_to_debug = log_to_debug.parent
        
def setup_root_logger():
    # Get the root logger and set it to DEBUG level.
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # print("Octo: got logger", root_logger)
    # dump_logger_hierarchy("Octo 1", root_logger)

    # Create a rotating log handler with each file 100 megabytes and
    # 10 files for a total of one gigabyte logging.
    handler = RotatingFileHandler("ts.log", maxBytes=10**8, backupCount=10)
    handler.setLevel(logging.DEBUG)

    # Set the formatter to prefix the log message with the date, name,
    # and log level.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the root logger. We're now all set up.
    root_logger.addHandler(handler)

import socket
def get_ip():
    IP = 'unknown'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # doesn't even have to be reachable:
        s.connect(('192.168.1.1', 80))

        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == "__main__":

    # Setup logging first of all

    setup_root_logger()
    setup_local_logger(__name__)

    # The first log entry will be the config ID.
    config_id = get_touchscreen_commit_id()

    ip_addr = get_ip()
    id_message = "IP: %s, Config ID: %s" % (ip_addr, config_id)
    
    print("******************************************************************************")
    print("re:3D touchscreen starting. " + id_message)
    print("******************************************************************************")

    _log("******************************************************************************")
    _log("* re:3D touchscreen starting. " + id_message)
    _log("******************************************************************************")
    
    #################################################################
    # This is the octoprint section

    # _log("Setting up OctoPrint")

    # Initialize settings
    settings = octoprint.settings.settings(True)

    # Initialize plugin manager
    plugin.plugin_manager(True)

    # Initialize profile manager
    profile_manager = profile.PrinterProfileManager()

    profile_manager.save(gigabot_profile, allow_overwrite = True, make_default = True)

    # Create an analysis queue
    analysis_queue = analysis.AnalysisQueue({})

    # Create the file manager
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
        sys.exit(1)
            
    # persona = Personality(False, "/media/plloppii", "/home/plloppii/devel/gcode-cache")

    storage_managers = dict()
    local_storage_manager = storage.LocalFileStorage(persona.localpath)
    storage_managers[octoprint.filemanager.FileDestinations.LOCAL] = local_storage_manager

    file_manager = octoprint.filemanager.FileManager(analysis_queue, None, None, initial_storage_managers=storage_managers)

    # debug_event_listener = DebugEventListener()
    jt_callback = JTCallback()

    printer = Printer(file_manager, analysis_queue, profile_manager)
    printer.register_callback(jt_callback)

    event_listener = JTEventListener()

    printer_if = PrinterIF(printer)

    #################################################################
    # This is the touchscreen section

    # _log("Setting up touchscreen UI")

    # print("Starting data threads.")
    # _log("Starting data threads.")

    # Can we get rid of these now?
    data_thread = g_data()
    client_conn = g_client(data_thread)
    serial_conn = g_serial(data_thread)
    data_thread.start()

    # print("Creating the UI")
    app = QtWidgets.QApplication(sys.argv)

    properties = {}
    config_path = Path(__file__).parent.absolute().__str__() + "/config.properties"
    for line in open(config_path):
        properties[line.split("=")[0]] = line.split("=")[1].strip()

    app.setApplicationName(properties["name"])
    app.setApplicationVersion(properties["version"])

    display = TouchDisplay(client_conn, printer_if, persona)
    display.SoftwareVersion.setText(id_message)
    display.show()

    # print("Starting the events flow")
    event_manager.fire(octoprint.events.Events.STARTUP)

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

    wd_thread = WatchdogThread(display.print_pop, persona.watchpoint,
                               current_path, persona.localpath)

    usb_signal_tup = wd_thread.get_usb_signals()
    display.print_pop.set_usb_mount_signals(usb_signal_tup)

    usb_content_signal = wd_thread.get_usb_content_signal()
    display.print_pop.set_usb_content_signal(usb_content_signal)

    local_content_signal = wd_thread.get_local_content_signal()
    display.print_pop.set_local_content_signal(local_content_signal)

    display.print_pop.set_storage_manager(local_storage_manager)

    # print("Connecting the printer (DEBUG USE ONLY)")
    # printer.connect("/dev/tty.usbserial-DN02B57Q", 250000)
    # printer.connect("/dev/tty.usbserial-143320", 115200)

    # print("Entering the main UI loop")
    # _log("Entering the main UI loop")
    app.exec_()
