# import os
# import stat
import psutil

class MountFinder:

    # Look through all the mounted filesystems, and try to guess which
    # one is the mount point for removable media. Return a list of
    # those that might be removable media.

    @staticmethod
    def thumbdrive_candidates():

        # Start with an empty list of candidates
        candidates = []

        # Get the list of mounted filesystems (False argument means
        # only return actual physical drives and ignore stuff like 
        partitions = psutil.disk_partitions(False)

        # Loop through the list and return the first that is (a)
        # mounted on a mount point that is probably a USB thumb drive,
        # or (b) is a windows-type filesystem (as most thumb drives
        # tend to be).

        for partition in partitions:

            # Is it?
            if MountFinder._is_thumb_drive(partition):

                # Might be! Add to the list of candidates
                candidates.append(partition.mountpoint)

            # dev = os.stat(m)[stat.ST_DEV]
            # major = os.major(dev)
            # minor = os.minor(dev)

            # print(p, "major: %d, minor: %d" % (major, minor))

        # Return the list of candidates
        return candidates

    @staticmethod
    def is_thumb_drive(path):
        
        # We need to get the partition object that corresponds to this
        # mount point. The psutils package doesn't seem to offer a way
        # to go from a path directly to a partition object, so we'll
        # just get them all, then look for one whose mountpoint
        # matches the given path. Not a great way to do it, but
        # mitigating factors are that we won't have to do this very
        # often, there typically aren't many mount points, and the
        # disk_partitions call seems very fast.

        partitions = psutil.disk_partitions(False)

        for partition in partitions:

            if partition.mountpoint == path:
                # Good, we've found the matching mountpoint. Now let
                # _is_thumb_drive determine whether it's probably a
                # thumb drive:
                return MountFinder._is_thumb_drive(partition)

    @staticmethod
    def _is_thumb_drive(partition):

        # Detect whether the mount point is a USB-type mount point.
        if False:
            pass

        # print("Partition type = <%s>" % partition.fstype)

        # Detect whether the filesystem type is a windows-type fs.
        if (partition.fstype == "msdos") or (partition.fstype == "exfat") or (partition.fstype == "vfat"):
            return True

        return False
        

if __name__ == "__main__":

    print("MountFinder test")

    path_list = MountFinder.thumbdrive_candidates()
    print("Best guesses:", path_list)

    print()
    print("Looping over filesystems to call is_thumb_drive:")
    
    partitions = psutil.disk_partitions(False)
    for p in partitions:

        isitq = MountFinder.is_thumb_drive(p.mountpoint)
        print("    <%s> is maybe a thumb drive?," % p.mountpoint, isitq)
