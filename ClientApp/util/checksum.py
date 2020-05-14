
import subprocess
import os
from pathlib import Path

def validate_checksum(verifyfile, verifyscript):

    #Calculate the checksum with the script path
    if(Path(verifyscript).is_file()):
        rtn = subprocess.check_output(verifyscript, shell=True)
        calculated_checksum = rtn.decode("utf-8").strip()
    else:
        print("md5check.sh script could not be found!")
        return

    if(Path(verifyfile).is_file()):
        with open(verifyfile, "r") as f:
            given_checksum = f.read().strip()
    else:
        print("md5verify file could not be found!!")
        return

    if(given_checksum == calculated_checksum):
        print("checksum validated!")
    else:
        print("checksum did not match!\n" + given_checksum, " ", calculated_checksum)