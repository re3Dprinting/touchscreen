class Personality:
    def __init__(self, user, watchpoint, localpath, logpath, touchscreenpath):
        """Personality object that defines the parameters of the machine the touchscreen application is being ran on.

        Arguments:
            user {[type]} -- [description]
            watchpoint {[type]} -- [description]
            localpath {[type]} -- [description]
            logpath {[type]} -- [description]
            touchscreenpath {String} -- The location of the touchscreen src files (ClientApp) dir
        """
        self.user = user
        self.watchpoint = watchpoint
        self.localpath = localpath
        self.logpath = logpath
        #Fetch the touchscreen path (ClientApp dir), gitrepo (touchscreen dir), and root directory(re3d dir)
        self.touchscreenpath = touchscreenpath.__str__()
        self.gitrepopath = touchscreenpath.parent.__str__()
        self.rootpath = touchscreenpath.parent.parent.__str__()
