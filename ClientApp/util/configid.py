import os
import subprocess

class BuildID:
    pass

# Note: WILL NOT WORK if any arguments have embedded spaces.

def runcommand(cmd_string):
    cmd_array = cmd_string.split()

    res = subprocess.run(cmd_array, capture_output=True, text=True)

    return res.stdout

def get_touchscreen_commit_id():
    pushed = os.getcwd()
    os.chdir("../touchscreen/")

    cmd = "git log -n 1 --pretty='%h'"

    output = runcommand(cmd)
    output = output.split('\n')[0]

    commit_id = output[1:-2]

    cmd = "git status --short"
    output = runcommand(cmd)
    output = output.split('\n')

    modfile = False
    unkfile = False

    for s in output:
        # print("Checking string <%s>" % s)
        if s == "":
            continue

        # Select the first two characters of the line.
        s = s[0:2]

        # Most files will have this status
        if s == '  ':
            continue

        # New and unknown files?
        if s == '??':
            unkfile = True

        # If the file is not unknown, but has non-blank status, assume
        # it's a modified file.
        else:
            modfile = True
            
    id_string = commit_id

    if modfile:
        id_string += " [modified]"

    if unkfile:
        id_string += " [newfiles]"

    os.chdir(pushed)

    return id_string
    

if __name__ == "__main__":
    id_string = get_touchscreen_commit_id()

    print(id_string)

