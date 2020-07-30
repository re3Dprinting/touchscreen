### A class to watch as filesystems are mounted and unmounted, and
### notify the UI when a USB thumb drive is connected.

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from PyQt5.QtCore import QObject, pyqtSignal

from .mountpointwatcher import MountpointWatcher
from .contentwatcher import ContentWatcher

class ContentTracker(QObject, FileSystemEventHandler):

    # PyQt signals have to be created here. The QObject constructor
    # will bind them to local names.
    create_signal = pyqtSignal(str)
    delete_signal = pyqtSignal(str)
    content_signal = pyqtSignal(str)

    # Constructor
    def __init__(self, watch_path):

        # MUST call the QObject constructor to ensure that the signals
        # get correctly bound.
        super(ContentTracker, self).__init__()

        self.watch_path = watch_path

        # Create the watcher object; it is called by the observer
        # whenever content in the watch path changes.
        self.content_watcher = ContentWatcher(self)

        # Create the observer; it watches the content path and calls
        # callbacks on the watcher, which then notifies us.
        self.create_content_observer(self.watch_path)

    def create_content_observer(self, path):

        # Create, initialize, and start the content observer.
        self.content_observer = Observer()

        # Use recursive mode to ensure we watch every file and
        # directory within the watch path.
        self.content_observer.schedule(self.content_watcher, path,
                                       recursive=True)

        # Start it running
        self.content_observer.start()

    # def delete_content_observer(self):
    #     if self.content_observer is not None:
    #         self.content_observer.stop()
    #         del self.content_observer

    def get_content_signal(self):
        return self.content_signal

    def content_modified(self, path):
        self.content_signal.emit(path)
