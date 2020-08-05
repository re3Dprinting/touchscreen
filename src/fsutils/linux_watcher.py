from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher(FileSystemEventHandler):
    def __init__(self):
        self.whatthe_observer = Observer()
#        self.whatthe_observer.schedule(self, "/media/pi", recursive=False)
        self.whatthe_observer.schedule(self, "/media/", recursive=False)
        self.whatthe_observer.start()

    def on_created(self, event):
        print("mpw on_created", event.src_path)
        
    def on_deleted(self, event):
        print("mpw on_deleted", event.src_path)

if __name__ == "__main__":

    print("Linux watcher test")

    watcher = Watcher()

    while True:
        pass
