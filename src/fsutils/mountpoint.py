import os

class MountPoint:

    def __init__(self, path):

        self.path = path

        if os.path.islink(path):
            self.actual_path = os.readlink(path)
        else:
            self.actual_path = path
            
