### A class to watch as filesystems are mounted and unmounted, and
### notify the UI when a USB thumb drive is connected.

import os
import time
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from PyQt5.QtCore import QObject, pyqtSignal

from .mountfinder import MountFinder
from .mountpoint import MountPoint
from .mountpointwatcher import MountpointWatcher
from .contentwatcher import ContentWatcher

class USBTracker(QObject, FileSystemEventHandler):

    create_signal = pyqtSignal(MountPoint)
    delete_signal = pyqtSignal(str)
    content_signal = pyqtSignal(str)

    def __init__(self, watch_path, initial_path, contentonly=False):
        super(USBTracker, self).__init__()
        
        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("USBTracker __init__()")

        self.watch_path = watch_path
        self.current_mountpoint = MountPoint("")

        # print("Watch path = <%s>" % watch_path)
        # print("Initial path = <%s>" % initial_path)

        self._log("Initializing with watch path = <%s>, initial path = <%s>" % (watch_path, initial_path))

        self.content_watcher = ContentWatcher(self)
        self.mountpoint_watcher = MountpointWatcher(self)
        # self.whatthe_watcher = MountpointWatcher(self)

        if initial_path != "":
            self.mountpoint_created(MountPoint(initial_path))

        self.create_mount_observer()

        # if contentonly:
        #     print("Content only")
        # else:
        #     print("NOT content only")

    def _log(self, message):
        self._logger.debug(message)

    def create_mount_observer(self):
        self.mount_observer = Observer()
        self.mount_observer.schedule(self.mountpoint_watcher, self.watch_path, recursive=False)
        self.mount_observer.start()

    def delete_mount_observer(self):
        if self.mount_observer is not None:
            self.mount_observer.stop()
            del self.mount_observer
            self.mmount_observer = None

    def create_content_observer(self, path):
        self.content_observer = None
        self._log("creating content observer on <%s>" % path)
        return

        # self.content_observer = Observer()
        # self.content_observer.schedule(self.content_watcher, path, recursive=True)
        # self.content_observer.start()

    def delete_content_observer(self):
        if self.content_observer is not None:
            self.content_observer.stop()
            self.content_observer.unschedule_all()
            del self.content_observer
            self.content_observer = None

    def get_mount_signals(self):
        return (self.create_signal, self.delete_signal)

    def get_content_signal(self):
        return self.content_signal

    def mountpoint_created(self, mountpoint):
        self._log("MOUNTPOINT CREATED: path <%s>, actual <%s>, Current is: <%s>, current actual: <%s>" % (mountpoint.path, mountpoint.actual_path, self.current_mountpoint.path, self.current_mountpoint.actual_path))

        self.mountpoint = mountpoint

        # The MountFinder.is_thumb_drive (below) relies on a list of
        # partitions, but sometimes there are occasions when we
        # receive an event indicating that a thumb drive has been
        # mounted, but the psutil.disk_partitions call does NOT
        # include the new mount point in the partitions list. A short
        # delay will allow the partitions list catch up to the now
        # mount point.
        # time.sleep(0.1)

        path = mountpoint.path
        actual_path = mountpoint.actual_path

        if MountFinder.is_thumb_drive(actual_path) and path.startswith(self.watch_path):
            self.create_content_observer(actual_path)
            self.current_mountpoint = mountpoint
            self.create_signal.emit(mountpoint)

    def mountpoint_deleted(self, path):
        self._log("Mountpoint deleted: <%s> Current is: <%s>, current actual: <%s>" % (path, self.current_mountpoint.path, self.current_mountpoint.actual_path))

        if self.current_mountpoint.path == path:
            self.delete_signal.emit(path)
            self.current_mountpoint = MountPoint("")
            self.delete_content_observer()

        # self.delete_mount_observer()
        # self.create_mount_observer()

    def content_modified(self, path):
        self._log("Content modified: <%s>" % (path))
        self.content_signal.emit(path)

    # # These two functions override functions in the
    # # FileSystemEventHandler class, hooking us up into changes
    # # of the mount points.
    
    # def on_created(self, event):
    #     self.mountpoint_created(event.src_path)
        
    # def on_deleted(self, event):
    #     self.mountpoint_deleted(event.src_path)

    # def on_modified(self, event):
    #     print("This was modified: <%s>" % event.src_path)

    # def __del__(self):
    #     self.mount_observer.join()
