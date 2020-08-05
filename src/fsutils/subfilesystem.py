import os
import os.path
import tarfile, zipfile
from threading import Thread
from pathlib import Path
import shutil
import datetime
import random

from fsutils.file import File
from fsutils.checksum import validate_checksum

class SubFileSystem():
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
                #Do not show touchscreen software updates within the printing menu. 
                if os.path.isfile(entry.path+"/md5verify"): continue
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

    
    #Similar to the list function above, try to fetch the toucchscreen software updates
    #Files can be either zipped or tar
    def list_ts_software_updates(self, userupdate_signal):
        updates = []
        tmp_path = self.rootdir+"/.tmp"+ str(random.getrandbits(64))

        #Create two iterators, one for deleting the previous tmp file, and one for checking for usb software. 
        try:
            it = os.scandir(self.abspath)
            it2 = os.scandir(self.abspath)
        except:
            return updates
        
        #Delete the other tmp files in another thread. 
        for f in it2:
            if(f.name.startswith(".tmp")):
                Thread(target = lambda : os.system("rm -rf "+self.rootdir+"/"+f.name)).start()

        os.mkdir(tmp_path)
        
        for entry in it:
            name = entry.name
            displayname = name
            extract_path = None
            valid = False

            if name.startswith("."):
                continue
            elif entry.is_dir():
                md5verify_path = entry.path + "/md5verify"
                md5check_path = entry.path + "/md5check.sh"
                if (Path(md5verify_path).is_file() and 
                    Path(md5check_path).is_file()):
                    if(validate_checksum(md5verify_path, md5check_path)):
                        valid = True
                        # print("Found dir with valid touchscreen application")
                type = "d"
            elif(tarfile.is_tarfile(entry.path)):
                tar_name = displayname.replace(".tar.gz","").replace(".tar","")

                curr_tar = tarfile.open(entry.path, "r")
                total_files = len(curr_tar.getmembers())

                md5verify_path = tar_name + "/md5verify"
                md5check_path = tar_name + "/md5check.sh"
                
                #Check if md5verify and md5check exists, then extract and perform md5check on files.
                if(md5verify_path in curr_tar.getnames() and
                    md5check_path in curr_tar.getnames()):

                    extracted_files = 0
                    userupdate_signal.emit(displayname, False)
                    for tar in curr_tar.getmembers():
                        extracted_files += 1
                        progress = displayname[:25]+".. %.0f %%" % (extracted_files *100 /total_files)
                        userupdate_signal.emit(progress, True)
                        curr_tar.extract(tar, path=tmp_path)

                    # curr_tar.extractall(path=tmp_path)
                    if(validate_checksum(tmp_path+"/"+md5verify_path, tmp_path+"/"+md5check_path)):
                        valid = True
                        extract_path = tmp_path+"/"+tar_name
                        # print("Found tar with valid touchscreen application!")
                type = "t"
            elif(zipfile.is_zipfile(entry.path)):
                zip_name = displayname.replace(".zip","")+"/"

                curr_zip = zipfile.ZipFile(entry.path)
                uncompress_size = sum([zinfo.file_size for zinfo in curr_zip.filelist])

                md5verify_path = zip_name + "md5verify"
                md5check_path = zip_name + "md5check.sh"
                
                if(md5verify_path in curr_zip.namelist() and
                    md5check_path in curr_zip.namelist()):

                    extracted_size = 0
                    userupdate_signal.emit(displayname, False)
                    for file in curr_zip.infolist():
                        extracted_size += file.file_size
                        progress = displayname[:25]+".. %.0f %%" % (extracted_size * 100/uncompress_size)
                        userupdate_signal.emit(progress, True)
                        curr_zip.extract(file, path=tmp_path)
                                   
                    curr_zip.extractall(path=tmp_path)
                    if(validate_checksum(tmp_path+"/"+md5verify_path, tmp_path+"/"+md5check_path)):
                        valid = True
                        extract_path = tmp_path+"/"+zip_name
                        # print("Found zip with valid touchscreen application!")
                type = "z"            
            
            if(not valid): continue
            
            statinfo = entry.stat()
            timestamp = datetime.datetime.fromtimestamp(statinfo.st_mtime).strftime('%I:%M%p %m/%d/%y')

            size = statinfo.st_size
            if self.cwd == "":
                rel_path = name
            else:
                rel_path = self.cwd + "/" + name
            abs_path = self.abspath + "/" + name
            the_update = File(name, displayname, rel_path, abs_path, size, type, extract_path, timestamp)
            updates.append(the_update)
        
        updates = sorted(updates)
        return updates
