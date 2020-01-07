### A class to watch as filesystems are mounted and unmounted, and
### notify the UI when a USB thumb drive is connected.

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from PyQt5.QtCore import QObject, pyqtSignal

from .mountfinder import MountFinder
from .mountpointwatcher import MountpointWatcher
from .contentwatcher import ContentWatcher

class ContentTracker(QObject, FileSystemEventHandler):

    create_signal = pyqtSignal(str)
    delete_signal = pyqtSignal(str)
    content_signal = pyqtSignal(str)

    def __init__(self, watch_path):
        super(ContentTracker, self).__init__()
        
        self.watch_path = watch_path

        print("Watch path = <%s>" % watch_path)

        self.content_watcher = ContentWatcher(self)

    def create_content_observer(self, path):
        # print("creating content observer on <%s>" % path)
        self.content_observer = Observer()
        self.content_observer.schedule(self.content_watcher, path, recursive=True)
        self.content_observer.start()

    def delete_content_observer(self):
        if self.content_observer is not None:
            self.content_observer.stop()
            del self.content_observer

    def get_content_signal(self):
        return self.content_signal

    def content_modified(self, path):
        print("Content modified: <%s>" % (path))
        self.content_signal.emit(path)
