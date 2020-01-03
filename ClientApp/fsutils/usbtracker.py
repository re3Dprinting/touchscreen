from  .mountfinder import MountFinder

### A class to watch as filesystems are mounted and unmounted, and
### notify the UI when a USB thumb drive is connected.
class USBTracker:

    def __init__(self, ui):
        self.ui = ui
        self.current = ""
        
    def mountpoint_created(self, path):
        print("Mountpoint created: <%s> Current is: <%s>" % (path, self.current))
        if MountFinder.is_thumb_drive(path):
            self.ui.update_usb_create(path)
            self.current = path

    def mountpoint_deleted(self, path):
        print("Mountpoint deleted: <%s> Current is: <%s>" % (path, self.current))
        if self.current == path:
            self.ui.update_usb_delete(path)
            self.current = ""
