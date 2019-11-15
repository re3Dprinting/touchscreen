import sys
import time
import logging
from watchdog.observers import Observer
#from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class my_handler(FileSystemEventHandler):

    def __init__(self, ui):
        self.ui = ui

    def on_created(self, event):
        self.ui.update_create(event.src_path)
        
    def on_deleted(self, event):
        self.ui.update_delete(event.src_path)

import time
from PyQt5.QtCore import QThread


class WatchdogThread(QThread):

    def __init__(self, ui):
        QThread.__init__(self)
        self.ui = ui

    def __del__(self):
        self.wait()

    def run(self):
        path = "/Volumes"
        event_handler = my_handler(self.ui)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()
        while(True):
            time.sleep(1)
