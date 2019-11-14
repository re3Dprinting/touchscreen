from builtins import object
from functools import total_ordering


@total_ordering
class File:
    def __init__(self, name="", displayname="", size=0, type='u'):
        self.name = name
        self.displayname = displayname
        self.size = size
        self.type = type

        # Comparename is the name to be used in filename comparisons,
        # for purposes of sorting. If we want filenames to do a
        # case-sensitive sort, then set comparename equal to name. For
        # a case-insensitive sort (the default), set comparename equal
        # to name.lower(). We pre-computer comparename so we don't
        # repeatedly call lower() in the comparison operators. It
        # takes a bit more memory, but is a bit more efficient.
        self.comparename = self.name.lower()

    def __eq__(self, other):
        return (self.comparename, self.size) == \
               (other.comparename, other.size)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.comparename, self.size) < \
               (other.comparename, other.size)
