from os.path import *

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time
from PyQt5.QtCore import QThread

class my_handler(FileSystemEventHandler):

    def __init__(self):
        pass

    def on_created(self, event):
        print("Created:", event.src_path)
        
    def on_deleted(self, event):
        print("Deleted:", event.src_path)

path = "/Users/jct/localgcode"

if __name__ == "__main__":

        if not exists(path):
            print("Path does not exist:", path)
            sys.exit()

        event_handler = my_handler()
        
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()

        while(True):
            time.sleep(1)
