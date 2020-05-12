class Personality:
    def __init__(self, user, fullscreen, watchpoint, localpath, logpath, touchscreenpath):
        self.user = user
        self.fullscreen = fullscreen
        self.watchpoint = watchpoint
        self.localpath = localpath
        self.logpath = logpath
        #Fetch the touchscreen path (ClientApp dir), gitrepo (touchscreen dir), and root directory 
        self.touchscreenpath = touchscreenpath.__str__()
        self.gitrepopath = touchscreenpath.parent.__str__()
        self.rootpath = touchscreenpath.parent.parent.__str__()
