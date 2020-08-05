import time
import logging
import psutil
from fsutils.ostype import *

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
        # /proc.
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

        # Return the list of candidates
        return candidates

    @staticmethod
    def _log(message):
        logger = logging.getLogger(__name__)
        logger.debug(message)

    @staticmethod
    def is_thumb_drive(path):

        time.sleep(0.1)

        # We need to get the partition object that corresponds to this
        # mount point. The psutils package doesn't seem to offer a way
        # to go from a path directly to a partition object, so we'll
        # just get them all, then look for one whose mountpoint
        # matches the given path. Not a great way to do it, but
        # mitigating factors are that we won't have to do this very
        # often, there typically aren't many mount points, and the
        # disk_partitions call seems very fast.

        MountFinder._log("Trying to determine whether <%s> is a thumb drive." % path)

        mountpoint_matched = False
        attempts = 1

        while (not mountpoint_matched) and (attempts <= 10):

            partitions = psutil.disk_partitions(False)
            MountFinder._log("Attempts to check mountpoint: %d" % attempts)

            time.sleep(1.0)

            for partition in partitions:
                MountFinder._log("  checking partition: <%s>" % partition.mountpoint)

                if partition.mountpoint == path:
                    mountpoint_matched = True
                    # Good, we've found the matching mountpoint. Now let
                    # _is_thumb_drive determine whether it's probably a
                    # thumb drive:
                    return MountFinder._is_thumb_drive(partition)

            attempts += 1


    @staticmethod
    def _is_thumb_drive(partition):

        # Detect whether the mount point is a USB-type mount
        # point.  We're going to rely on the (admittedly naive)
        # assumption that only thumb drives will have the nosuid
        # mount option. If the mount point doesn't have this
        # option, assume it's not a thumb drive. (Note: this only
        # works for linux.)

        MountFinder._log("Partition <%s>: type is <%s>" % (partition.mountpoint, partition.fstype))

        # if os_is_linux():
        #     MountFinder._log("    testing for linux, partition options <%s>" % partition.opts)
        #     if ("nosuid" in partition.opts):
        #         return True

        # elif os_is_macos():
        #     MountFinder._log("    testing for macOS, partition type <%s>" % partition.fstype)

        #     # Detect whether the filesystem type is a windows-type
        #     # fs. Most thumb drives are formatted as one of these types.
        if (partition.fstype == "msdos") or (partition.fstype == "exfat") or (partition.fstype == "vfat"):
            if not partition.device.startswith("/dev/mmc"):
                MountFinder._log("    It IS a thumb drive.")
                return True

        # If we can't determine the operating system, we can't
        # recognize a thumb drive.
        MountFinder._log("    It is not a thumb drive.")
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
