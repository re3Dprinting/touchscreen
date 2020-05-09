from pathlib import Path
import shutil
from git import Repo, Git
import os
import json


#Search for a backup directory within the re3d directory. 
#   -If the backup exists (which is created on a update)
#   -Copy the back-up file over to the original (including the .git files)
def restore_backup(personality):
    #Grab the current directory were the git repository is initialized.
    backup_path = personality.gitrepopath + "_backup"
    broken_path = personality.gitrepopath+"_broken"

    if(Path(backup_path).is_dir()):
        #Move the current path to a label broken path
        shutil.move(personality.gitrepopath, broken_path)
        #Copy the backup over to current path
        shutil.copytree(backup_path, personality.gitrepopath)
        #remove the broken path.
        shutil.rmtree(broken_path)
