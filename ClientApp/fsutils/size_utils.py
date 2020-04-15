import os
import math
import time
import glob

from constants import k_logname

def filesys_blocks_free(path):
    vol_stats = os.statvfs(path)
    blocks_avail = vol_stats.f_bavail
    block_size = vol_stats.f_frsize
    return (block_size, blocks_avail)

def file_blocks_used(file_path, block_size):
    file_stats = os.stat(file_path)
    file_bytes_used = file_stats.st_size
    file_blocks_used = math.ceil(file_bytes_used / block_size)
    return file_blocks_used

def ensure_sufficient_space_for_file(gcode_dest_dir, log_dir, log_size, gcode_file):

    print("Input parameters:")
    print("  gcode_dest_dir =", gcode_dest_dir)
    print("  log_dir = ", log_dir)
    print("  log_size = %d bytes" % log_size)
    print("  gcode_file =", gcode_file)

    # First, figure out how much room is available in the destination
    # directory.
    (filesys_block_size, filesys_blocks_avail) = filesys_blocks_free(gcode_dest_dir)

    print()
    print("%s block size = %d bytes" % (gcode_dest_dir, filesys_block_size))
    print("blocks available = %d" % filesys_blocks_avail)

    # Now figure out how many blocks will be required for the
    # specified file. NOTE: compute file size in destination blocks.
    print()
    file_blocks_req = file_blocks_used(gcode_file, filesys_block_size)
    print("file blocks required = %d" % file_blocks_req)

    # Arbitrarily add a buffer to the amount of log we need
    # log_size += (log_size / 10)

    # Now figure out how many blocks are required for the log
    log_blocks_req = log_size / filesys_block_size
    print("log blocks required = %d" % log_blocks_req)

    total_blocks_req = file_blocks_req + log_blocks_req
    print("total blocks required = %d" % total_blocks_req)

    # Compute the number of blocks already in use for the log
    print()
    log_blocks_already_in_use = log_file_cumulative_size(log_dir)
    print()

    # We can deduct the number of log file blocks already in use from
    # the number required
    total_blocks_req -= log_blocks_already_in_use
    print("total blocks required, adjusted for current log size = %d" % total_blocks_req)

    # If we have enough room, we're done.
    if filesys_blocks_avail >= total_blocks_req:
        print("Enough blocks are available, nothing to do. (%d >= %d)" % (filesys_blocks_avail, total_blocks_req))
        return True
    else:
        print("Not enough blocks available. (%d < %d)" % (filesys_blocks_avail, total_blocks_req))

        return make_blocks_available(gcode_dest_dir, total_blocks_req)

def filekey(filename):
    return os.stat(filename).st_mtime

def make_blocks_available(gcode_dest_dir, total_blocks_req):
    # Strategy: sort the gcode files by least recently modified
    # (oldest first). Then loop through them, adding up the file sizes
    # until the total size meets or exceeds tho total number of blocks
    # needed. At that point, delete the files, oldest firest. If the
    # total does not exceed the number required, then delete NO
    # files. Note that this LRU algorithm assumes that files are
    # touched every time they are printed, so that their
    # "modification" time is updated, even though the files are not
    # actually modified when re-printed.

    (filesys_block_size, filesys_blocks_avail) = filesys_blocks_free(gcode_dest_dir)

    print()
    print("Making room for %d blocks in gcode destination directory %s" % (total_blocks_req, gcode_dest_dir))

    gcode_files = glob.glob(gcode_dest_dir + "/*.gcode")
    gcode_files = gcode_files + glob.glob(gcode_dest_dir + "/*.gco")
    gcode_files = gcode_files + glob.glob(gcode_dest_dir + "/*.g")
    gcode_files = gcode_files + glob.glob(gcode_dest_dir + "/*.GCODE")
    gcode_files = gcode_files + glob.glob(gcode_dest_dir + "/*.GCO")
    gcode_files = gcode_files + glob.glob(gcode_dest_dir + "/*.G")

    # Sort the files by modification time, oldest first
    gcode_files = sorted(gcode_files, key=filekey)

    to_delete = []
    to_delete_blocks = 0

    for file in gcode_files:
        # print_file(file, filesys_block_size)
        file_block_size = file_blocks_used(file, filesys_block_size)

        to_delete_blocks += file_block_size
        to_delete.append(file)

        print("%8d blocks, %8d total, %s" % (file_block_size, to_delete_blocks, file))
        

        if to_delete_blocks >= total_blocks_req:
            print("Identified files to delete totalling %d blocks." % to_delete_blocks)
            # We've identified enough deletable files to make the room
            # we need. Delete files and return.

            print()
            for file in to_delete:
                print("Unlink %s" % file)

            return True

    print()
    print("UNABLE to find enough files to make sufficient room; none deleted")
    return False

def print_file(file, filesys_block_size):
    s = os.stat(file)
    size = file_blocks_used(file, filesys_block_size)
    print("%12d %s %s" % (size, time_str(s.st_mtime), file))

def time_str(ltime):
    ltime_struct = time.localtime(ltime)
    ltime_str = time.strftime("%b %d %Y", ltime_struct)
    return ltime_str

def log_file_cumulative_size(log_dir):
    (filesys_block_size, filesys_blocks_avail) = filesys_blocks_free(log_dir)
    logfiles = glob.glob(log_dir + "/" + k_logname + "*")

    total_blocks = 0

    # print("Log file sizes:")
    for file in logfiles:
        size = file_blocks_used(file, filesys_block_size)
        total_blocks += size
        # print("  %s: %d blocks, total = %d" % (file, size, total_blocks))

    return total_blocks
