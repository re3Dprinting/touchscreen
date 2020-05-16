from pathlib import Path
from shutil import copyfile
from git import Repo, Git
import os
import json

#Load the properties from the json file, config.properties
#   -config.properties acts as a static file that all windows can access
#   -the permission is set if the specified. 
#   -if the config.properties file is not found, create it in the correct directory.
def get_properties(personality, permission = "Default"):
    properties = {"name": "", 
                "motherboard" : "", 
                "wifissd" : "",
                "wifipassword" : "",
                "permission" : ""
                }

    #Grab the config.properties file
    config_path = personality.rootpath + "/config.properties"
    example_config_path = personality.touchscreenpath + "/setup-files/config.properties"

    #If the file does not exist, move the file over to the correct directory. 
    if( not Path(config_path).is_file() and Path(example_config_path).is_file() ):
        copyfile(example_config_path, config_path)

    #Catch exception if config_path still does not exist. 
    with open(config_path, "r+") as config_in:
        loaded_properties = json.load(config_in)
        properties = {**properties, **loaded_properties}
        #Set the permission if specified. Otherwise, keep as default.
        if not permission == "Default" and "permission" in properties: 
            properties["permission"] = permission
            config_in.seek(0)
            json.dump(properties, config_in, indent=4)
            config_in.truncate()

    #Grab the version from the current git repository. 
    #Will have to be adjusted if the user is updating software locally!!!!

    try:
        repo = Repo(personality.gitrepopath)
        current_version = next((tag for tag in repo.tags if tag.commit == repo.head.commit), None)
        properties["version"] = current_version.name
    #If no tag found, check for current branch
    except AttributeError as e:
        properties["version"] = repo.active_branch.name
    #If no branch/repo found, default to local. 
    except Exception as e:
        properties["version"] = "Local"
        
    return properties