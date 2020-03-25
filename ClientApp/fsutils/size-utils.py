import os
import math
import time

def filesys_blocks_free(path):
    vol_stats = os.statvfs(path)
    blocks_avail = vol_stats.f_bavail
    block_size = vol_stats.f_frsize
    return (block_size, blocks_avail)

def file_blocks_used(path):
    vol_stats = os.statvfs(path)
    block_size = vol_stats.f_frsize
    file_stats = os.stat(path)
    file_bytes_used = file_stats.st_size
    file_blocks_used = (file_bytes_used / block_size) + 1
    return file_blocks_used

def filekey(file):
    return file.stat().st_mtime

def time_str(ltime):
    ltime_struct = time.localtime(ltime)
#    ltime_str = time.strftime("%H:%M:%S %b %d %Y", ltime_struct)
    ltime_str = time.strftime("%b %d %Y", ltime_struct)
    return ltime_str

def print_file(file):
    print("%10d %s %s" % (file.stat().st_size, time_str(file.stat().st_mtime), file.name))

def build_file_list(path):
    files = os.scandir(path)
    files = sorted(files, key=filekey)
    for file in files:
        print_file(file)
    return files

if __name__ == "__main__":
    vol_path = "/Volumes/Of Course I Still Love You"
    (x_block_size, x_blocks_free) = filesys_blocks_free(vol_path)
    print("OCISLY blocks free = %d." % x_blocks_free)
    print("OCISLY block size = %d." % x_block_size)
    
    f_file_name = "foo.out"
    f_file_path = vol_path + "/" + f_file_name
    f_blocks_used = file_blocks_used(f_file_path)
    print("%s blocks used = %d." % (f_file_path, f_blocks_used))
    
    b_file_name = "bar.out"
    b_file_path = vol_path + "/" + b_file_name
    b_blocks_used = file_blocks_used(b_file_path)
    print("%s blocks used = %d." % (b_file_path, b_blocks_used))

    print()

    build_file_list(vol_path + "/gcode-cache")
