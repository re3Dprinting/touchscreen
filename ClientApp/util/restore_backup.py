from pathlib import Path
import shutil
from git import Repo, Git
import os
import json
import logging


def setup_local_logger(name):
    global logger
    logger = logging.getLogger(name)


def _log(message):
    global logger
    logger.debug(message)


setup_local_logger(__name__)

# Search for a backup directory within the re3d directory.
#   -If the backup exists (which is created on a update)
#   -Copy the back-up file over to the original (including the .git files)


def restore_backup(personality, properties):
    if(personality.user != "pi" or properties["permission"] == "developer"):
        return

    # Grab the current directory were the git repository is initialized.
    backup_path = personality.gitrepopath + "_backup"
    broken_path = personality.gitrepopath+"_broken"

    if(Path(backup_path).is_dir()):
        _log("*** Restoring backup touchscreen software! ***")
        # Move the current path to a label broken path
        shutil.move(personality.gitrepopath, broken_path)
        # Copy the backup over to current path
        shutil.copytree(backup_path, personality.gitrepopath)
        # remove the broken path.
        shutil.rmtree(broken_path)
