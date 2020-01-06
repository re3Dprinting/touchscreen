from watchdog.events import FileSystemEventHandler
from watchdog.events import DirModifiedEvent

class ContentWatcher(FileSystemEventHandler):

    def on_modified(self, event):
        if type(event) is DirModifiedEvent:
            print("Got event:", event)
