import logging
from watchdog.events import FileSystemEventHandler

from .mountpoint import MountPoint

class MountpointWatcher(FileSystemEventHandler):

    def __init__(self, tracker):
        self.tracker = tracker

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("MountpointWatcher __init__")

    def _log(self, message):
        self._logger.debug(message)

    def dispatch(self, event):
        self._log("MountpointWatcher received dispatch.")
        super().dispatch(event)

    def on_created(self, event):
        self._log("MountpointWatcher received ON_CREATED <%s>" % event.src_path)
        mountpoint = MountPoint(event.src_path)
        self.tracker.mountpoint_created(mountpoint)
        
    def on_deleted(self, event):
        self._log("MountpointWatcher received on_deleted <%s>" % event.src_path)
        self.tracker.mountpoint_deleted(event.src_path)
