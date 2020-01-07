### A class to watch as filesystems are mounted and unmounted, and
### notify the UI when a USB thumb drive is connected.

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from PyQt5.QtCore import QObject, pyqtSignal

from .mountfinder import MountFinder
from .mountpointwatcher import MountpointWatcher
from .contentwatcher import ContentWatcher

class USBTracker(QObject, FileSystemEventHandler):

    create_signal = pyqtSignal(str)
    delete_signal = pyqtSignal(str)
    content_signal = pyqtSignal(str)

    def __init__(self, ui, watch_path, initial_path, contentonly=False):
        super(USBTracker, self).__init__()
        
        self.ui = ui
        self.watch_path = watch_path
        self.current_path = ""

        print("Watch path = <%s>" % watch_path)
        print("Initial path = <%s>" % initial_path)

        self.content_watcher = ContentWatcher(self)
        self.mountpoint_watcher = MountpointWatcher(self)

        if initial_path != "":
            self.mountpoint_created(initial_path)

        self.create_mount_observer()

        if contentonly:
            print("Content only")
        else:
            print("NOT content only")

    def create_mount_observer(self):
        self.mount_observer = Observer()
        self.mount_observer.schedule(self.mountpoint_watcher, self.watch_path, recursive=False)
        self.mount_observer.start()

    def create_content_observer(self, path):
        # print("creating content observer on <%s>" % path)
        self.content_observer = Observer()
        self.content_observer.schedule(self.content_watcher, path, recursive=True)
        self.content_observer.start()

    def delete_content_observer(self):
        if self.content_observer is not None:
            self.content_observer.stop()
            del self.content_observer

    def get_mount_signals(self):
        return (self.create_signal, self.delete_signal)

    def get_content_signal(self):
        return self.content_signal

    def mountpoint_created(self, path):
        # print("Mountpoint created: <%s> Current is: <%s>" % (path, self.current_path))
        if MountFinder.is_thumb_drive(path):
            self.create_content_observer(path)
            self.create_signal.emit(path)
            self.current_path = path

    def mountpoint_deleted(self, path):
        # print("Mountpoint deleted: <%s> Current is: <%s>" % (path, self.current_path))
        if self.current_path == path:
            self.delete_signal.emit(path)
            self.current_path = ""
            self.delete_content_observer()

    def content_modified(self, path):
        print("Content modified: <%s>" % (path))
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
