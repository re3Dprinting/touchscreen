from watchdog.events import FileSystemEventHandler
from watchdog.events import DirModifiedEvent

class ContentWatcher(FileSystemEventHandler):

    def __init__(self, tracker):
        self.tracker = tracker

    # def on_any_event(self, event):
    #     print("Any:", event)

    def on_modified(self, event):
        # print("Modified:", event)
        self.tracker.content_modified(event.src_path)

    def on_created(self, event):
        # print("Created: ", event)
        self.tracker.content_modified(event.src_path)

    def on_deleted(self, event):
        # print("Deleted: ", event)
        self.tracker.content_modified(event.src_path)

    def on_modified(self, event):
        # print("Modified: ", event)
        self.tracker.content_modified(event.src_path)

    def on_moved(self, event):
        # print("Moved: ", event)
        self.tracker.content_modified(event.src_path)

    

