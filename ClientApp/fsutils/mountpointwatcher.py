from watchdog.events import FileSystemEventHandler

class MountpointWatcher(FileSystemEventHandler):

    def __init__(self, tracker):
        self.tracker = tracker

    def dispatch(self, event):
        print("mpw DISPATCH!")
        super().dispatch(event)

    def on_created(self, event):
        print("mpw on_created", event.src_path)
        self.tracker.mountpoint_created(event.src_path)
        
    def on_deleted(self, event):
        print("mpw on_deleted", event.src_path)
        self.tracker.mountpoint_deleted(event.src_path)
