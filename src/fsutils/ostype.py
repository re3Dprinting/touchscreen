import sys

# Get the platform name.
plat = sys.platform

class ostype:
    def __init__(self):
        pass

def os_is_linux():

    if plat.startswith("linux"):
        return True

    return False

def os_is_macos():
    if  plat.startswith("darwin"):
        return True

    return False

