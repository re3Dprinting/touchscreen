
import subprocess
import os
from pathlib import Path

#Use the verifyscript to generate a md5sum and compare it to the verifyfile, which is a pregenerated md5sum.
#verifyfile contains the already generated md5sum in a text file. 
#verifyscript is the path to the md5generate script.
def validate_checksum(verifyfile, verifyscript):
    #Calculate the checksum with the script path
    if(Path(verifyscript).is_file()):
        cmd = "bash " + verifyscript
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        out, err = process.communicate()
        calculated_checksum = out.decode("utf-8").strip()
    else:
        print("md5check.sh script could not be found!")
        return False

    if(Path(verifyfile).is_file()):
        with open(verifyfile, "r") as f:
            given_checksum = f.read().strip()
    else:
        print("md5verify file could not be found!!")
        return False

    if(given_checksum != calculated_checksum):
        print("checksum did not match!\n" + given_checksum, " ", calculated_checksum)
        return False

    return True