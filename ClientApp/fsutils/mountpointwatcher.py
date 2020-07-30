import traceback
import logging
from util.log import tsLogger
from watchdog.events import FileSystemEventHandler

from .mountpoint import MountPoint

class MountpointWatcher(FileSystemEventHandler, tsLogger):

    def __init__(self, tracker):
        self.tracker = tracker

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log_d("MountpointWatcher __init__()")

    def dispatch(self, event):
        self._log_d("MountpointWatcher received dispatch.")
        super().dispatch(event)

    def on_created(self, event):
        try:
            self._log_d("MountpointWatcher received ON_CREATED <%s>" % event.src_path)
            mountpoint = MountPoint(event.src_path)
            self.tracker.mountpoint_created(mountpoint)
        except Exception:
            stack = traceback.format_exc()
            self._log_d(stack)
        
    def on_deleted(self, event):
        try:
            self._log_d("MountpointWatcher received on_deleted <%s>" % event.src_path)
            self.tracker.mountpoint_deleted(event.src_path)
        except Exception:
            stack = traceback.format_exc()
            self._log_d(stack)
