import sys
import time
import logging

from os.path import exists
from watchdog.observers import Observer

from .mountpointwatcher import MountpointWatcher
from .contentwatcher import ContentWatcher
from .usbtracker import USBTracker
from .contenttracker import ContentTracker

class WatchdogThread():

    def __init__(self, ui, mount_watch_path, initial_path, content_watch_path):

        self.mount_watch_path = mount_watch_path
        
        self.usb_tracker = USBTracker(mount_watch_path, initial_path, True)

        if not exists(self.mount_watch_path):
            print("*** ERROR: mount path does not exist")
            return

        self.local_tracker = ContentTracker(content_watch_path)

        # if initial_path != "":
        #     self.tracker.mountpoint_created(initial_path)

        # mountpoint_watcher = MountpointWatcher(self.tracker)

        # self.mount_observer = Observer()
        # self.mount_observer.schedule(mountpoint_watcher, self.mount_watch_path, recursive=False)
        # self.mount_observer.start()

        # content_watcher = ContentWatcher(ui)

        # self.content_observer = Observer()
        # self.content_observer.schedule(content_watcher, content_watch_path)
        # self.content_observer.start()

    def get_usb_signals(self):
        return self.usb_tracker.get_mount_signals()

    def get_usb_content_signal(self):
        return self.usb_tracker.get_content_signal()

    def get_local_content_signal(self):
        return self.local_tracker.get_content_signal()

    def __del__(self):
        # self.wait()
        # self.mount_observer.join()
        # self.content_observer.join()
        pass
