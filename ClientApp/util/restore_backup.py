from pathlib import Path
from shutil import copyfile
from git import Repo, Git
import os
import json


#Search for a backup directory within the re3d directory. 
#   -If the backup exists (which is created on a update)
#   -Copy the back-up file over to the original (including the .git files)
def restore_backup(personality):
    #Grab the current directory were the git repository is initialized.
    backup_path = personality.gitrepopath + "_backup"
    
    if(Path(backup_path).is_file()):
        print(backup_path, " found")
    else:
        print(backup_path, " not found")
