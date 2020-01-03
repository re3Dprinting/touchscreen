import sys
import time
import logging
from os import path
from os.path import *
from watchdog.observers import Observer
#from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

from fsutils.usbtracker import USBTracker

import time
from PyQt5.QtCore import QThread

class my_handler(FileSystemEventHandler):

    def __init__(self, tracker):
        self.tracker = tracker

    def on_created(self, event):
        self.tracker.mountpoint_created(event.src_path)
        
    def on_deleted(self, event):
        self.tracker.mountpoint_deleted(event.src_path)


class WatchdogThread(QThread):

    def __init__(self, ui, watch_path, current_path):
        QThread.__init__(self)
        self.ui = ui
        self.watch_path = watch_path
        self.tracker = USBTracker(ui)

        if current_path != "":
            self.tracker.mountpoint_created(current_path)

    def __del__(self):
        self.wait()

    def run(self):
        if not exists(self.watch_path):
            return

        event_handler = my_handler(self.tracker)
        observer = Observer()
        observer.schedule(event_handler, self.watch_path, recursive=False)
        observer.start()
        while(True):
            time.sleep(1)
