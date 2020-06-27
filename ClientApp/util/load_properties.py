from pathlib import Path
from shutil import copyfile
import git
import os
import json


def get_properties(personality, permission="Default"):
    """
    Load the properties from the json file, config.properties
    The 'permission' key:value pair is set if a value other that Default is specified.
    Load the example properties file if no config.properties file is found.

    Arguments:
        personality {Personality} -- Personality object for path references. 

    Keyword Arguments:
        permission {str} -- Set the permission level if a different permission level is set. (default: {"Default"})

    Returns:
        [dict] -- A map of the properties key value pairs. 
    """
    properties = {"name": "",
                  "motherboard": "",
                  "wifissd": "",
                  "wifipassword": "",
                  "permission": "",
                  "wifienabled": ""
                  }

    # Grab the config.properties file
    config_path = personality.rootpath + "/config.properties"
    example_config_path = personality.touchscreenpath + \
        "/setup-files/config.properties"

    # If the file does not exist, move the file over to the correct directory.
    if(not Path(config_path).is_file() and Path(example_config_path).is_file()):
        copyfile(example_config_path, config_path)

    with open(config_path, "r+") as config_in:
        loaded_properties = json.load(config_in)
        properties = {**properties, **loaded_properties}
        # Set the permission if specified. Otherwise, keep as default.
        if not permission == "Default" and "permission" in properties:
            properties["permission"] = permission
            config_in.seek(0)
            json.dump(properties, config_in, indent=4)
            config_in.truncate()

    # Grab the version from the current git repository.
    # Will have to be adjusted if the user is updating software locally!!!!

    try:
        repo = git.Repo(personality.gitrepopath)
    except git.InvalidGitRepositoryError as e:
        repo = git.Repo.init(personality.gitrepopath)

    # try:
    current_version = next(
        (tag for tag in repo.tags if tag.commit == repo.head.commit), None)
    if current_version == None:
        try:
            current_version = repo.active_branch.name
        except TypeError:
            current_version = "HEAD_detacted"
        except Exception e:
            current_version = "Local"
    else:
        current_version = current_version.name

    properties["version"] = current_version

    return properties


def get_software_details(readme_path):
    """
    Looks for the details of the latest release in the readme file.
    Parses the data between the beginning "---" and ending "---"
    Used for the descriptions of local USB updates.

    Arguments:
        readme_path {String} -- The path to the readme file that is going to be parsed in this function.
    """

    version = ""
    description = ""
    if(Path(readme_path).is_file()):
        with open(readme_path) as readme:
            copy = False
            for line in readme:
                if line.strip() == "---":
                    copy = True
                    continue
                elif line.strip() == "---" and (version != "" or description != ""):
                    break
                elif copy:
                    if line.strip() == "":
                        continue
                    elif line.strip()[0] == "v":
                        version = line.strip()
                    else:
                        description += line.strip()+"\n"
    return (version, description)
