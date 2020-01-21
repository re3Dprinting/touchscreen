from builtins import object
import os
import os.path
from .file import File

class SubFileSystem(object):
    def __init__(self, rootdir):
        self.files = []
        self.rootdir = rootdir
        self.cwd = ""
        self.abspath = ""
        self.setCwd("")
        self.level = 0
        self.dir_stack = []
        self.dir_stack.append(rootdir)

    def dumpstate(self, message):
        print()
        print("------")
        print(message)
        print("rootdir: <%s>" % self.rootdir)
        print("cwd: <%s>" % self.cwd)
        print("abspath: <%s>" % self.abspath)

    def setCwd(self, path):
        self.cwd = path
        self.abspath = os.path.abspath(self.rootdir + "/" + self.cwd)

    def depth(self):
        return self.level

    def cd(self, dir):
        if dir == "..":
            self.cdup()
            return

        self.dir_stack.append(self.cwd)
        self.level += 1
        self.setCwd(dir)

    def up(self):
        if self.level == 0:
            return

        self.level -= 1
        self.setCwd(self.dir_stack.pop())

    def list(self):
        self.files = []
        it = []

        # print("List <%s>" % self.cwd)
        # os.stat(self.rootdir + "/" + self.cwd)

        # os.stat(self.abspath)

        try:
            # Get the list of files in the current working directory
            it = os.scandir(self.abspath)

        # There's a number of exceptions that can occur in os.scandir,
        # mostly related to directories to which we do not have read
        # or execute permission. For all of these, simply act as if no
        # files have been found.
        except:
            # self.files is already empty. Return it.
            return self.files

        # Loop through the files, collecting some information in each
        for entry in it:

            # Start with the name
            name = entry.name
            displayname = name

            # Do not display nondirectory files that don't appear to
            # be gcode files
            if not entry.is_dir():
                if not (name.endswith(".gcode") or
                        name.endswith(".gco") or
                        name.endswith(".g")):
                    continue

            # Do some filtering. (To-do: create a filter class do do this)
            if name.startswith("."):
                continue

            if entry.is_dir():
                type = 'd'
            elif entry.is_file():
                type = 'f'
            elif entry.is_symlink():
                type = 'l'
            else:
                type = 'u'

            # Do some more filtering. (To-do: filter class)
            if type == 'l':
                continue

            # If the file is a directory, append a slash to the
            # display name this is how we visually distinguish
            # directories and folders from regular files.

            if type == 'd':
                displayname += "/"

            # Call stat to get information that includes the file size
            statinfo = entry.stat()
            size = statinfo.st_size

            if self.cwd == "":
                rel_path = name
            else:
                rel_path = self.cwd + "/" + name

            abs_path = self.abspath + "/" + name

            # Create a tuple and append it to the list of files
            the_file = File(name, displayname, rel_path, abs_path, size, type)
            self.files.append(the_file)

        # Lastly, return the list of file tuples
        self.files = sorted(self.files)
        return self.files

