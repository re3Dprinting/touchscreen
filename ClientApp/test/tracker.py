import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class tracker(FileSystemEventHandler):

    def __init__(self):
        observer = Observer()
        observer.schedule(self, "/usb/", recursive=True)
        observer.start()

    def on_created(self, event):
        print("on_create <%s>" % event.src_path)

    def on_deleted(self, event):
        print("on_deleted <%s>" % event.src_path)

if __name__ == "__main__":

    t = tracker()
    while True:
        time.sleep(1.0)
