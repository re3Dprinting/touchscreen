from dataclasses import dataclass
@dataclass
class Personality:
    """Personality object that defines the parameters of the machine the touchscreen application is being ran on.

    Arguments:
        user {[type]} -- [description]
        watchpoint {[type]} -- [description]
        gcodepath {[type]} -- [description]
        logpath {[type]} -- [description]
        touchscreenpath {String} -- The location of the touchscreen src files (ClientApp) dir
    """
    user:str
    watchpoint:str
    gcodepath:str
    logpath:str
    touchscreenpath:str
    def __post_init__(self):
        #Fetch the touchscreen path (ClientApp dir), gitrepo (touchscreen dir), and root directory(re3d dir)
        self.gitrepopath = self.touchscreenpath.parent.__str__()
        self.rootpath = self.touchscreenpath.parent.parent.__str__()
        self.touchscreenpath = self.touchscreenpath.__str__()
