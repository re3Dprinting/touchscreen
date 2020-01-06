from watchdog.events import FileSystemEventHandler

class MountpointWatcher(FileSystemEventHandler):

    def __init__(self, tracker):
        self.tracker = tracker

    def on_created(self, event):
        self.tracker.mountpoint_created(event.src_path)
        
    def on_deleted(self, event):
        self.tracker.mountpoint_deleted(event.src_path)
