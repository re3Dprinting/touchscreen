import os
import math
import time
import glob
import logging

from constants import k_logmaxbytes

from fsutils.size_utils import *

def filekey(file):
    return file.stat().st_mtime

def time_str(ltime):
    ltime_struct = time.localtime(ltime)
#    ltime_str = time.strftime("%H:%M:%S %b %d %Y", ltime_struct)
    ltime_str = time.strftime("%b %d %Y", ltime_struct)
    return ltime_str

def print_file(file):
    s = file.stat()
    size = s.st_size
    print("%12d %s %s" % (size, time_str(s.st_mtime), file.name))

def build_file_list(path):
    files = os.scandir(path)
    files = sorted(files, key=filekey)
    for file in files:
        print_file(file)
    return files

if __name__ == "__main__":
#    vol_path = "/Volumes/Of Course I Still Love You"
    vol_path = "/volumes/test-16"
    print("%s:" % vol_path)
    (x_block_size, x_blocks_free) = filesys_blocks_free(vol_path)
    print("blocks free = %d." % x_blocks_free)
    print("block size = %d." % x_block_size)
    
    # f_file_name = "foo.out"
    # f_file_path = vol_path + "/" + f_file_name
    # f_blocks_used = file_blocks_used(f_file_path)
    # print("%s blocks used = %d." % (f_file_path, f_blocks_used))
    
    # b_file_name = "bar.out"
    # b_file_path = vol_path + "/" + b_file_name
    # b_blocks_used = file_blocks_used(b_file_path)
    # print("%s blocks used = %d." % (b_file_path, b_blocks_used))

    print()
    build_file_list(vol_path)

    gcode_dest_dir = vol_path + "/gcode"
    gcode_log_dir = vol_path + "/log"
    #    gcode_file = gcode_dest_dir + "/a.out.gcode"
    gcode_file = "/Users/jct/200m.gcode"

    print()

    ensure_sufficient_space_for_file(gcode_dest_dir, gcode_log_dir, k_logmaxbytes, gcode_file)


    print()

    print("*** done ***")
