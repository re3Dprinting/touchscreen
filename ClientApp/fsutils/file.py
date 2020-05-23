from builtins import object
from functools import total_ordering


@total_ordering
class File:
    def __init__(self, name, displayname, rel_path, abs_path, size, type, extract_path=None, timestamp=None):
        self.name = name
        self.displayname = displayname
        self.relative_path = rel_path
        self.absolute_path = abs_path

        # Comparename is the name to be used in filename comparisons,
        # for purposes of sorting. If we want filenames to do a
        # case-sensitive sort, then set comparename equal to name. For
        # a case-insensitive sort (the default), set comparename equal
        # to name.lower(). We pre-computer comparename so we don't
        # repeatedly call lower() in the comparison operators. It
        # takes a bit more memory, but is a bit more efficient.
        self.comparename = self.name.lower()
        self.size = size
        self.type = type
        self.extract_path = extract_path
        self.timestamp = timestamp

    def dump(self):
        print("Name: <%s>" % self.name)
        print("Display name: <%s>" % self.displayname)
        print("Relative path: <%s>" % self.relative_path)
        print("Absolute path: <%s>" % self.absolute_path)
        print("Size: <%d> Type: <%s>" % (self.size, self.type))
        if(self.extract_path): print("Extracted path: <%s>" % self.extract_path)
        if(self.timestamp): print("Last modified: <%s>" % self.timestamp)

    def __eq__(self, other):
        return (self.comparename, self.size) == \
               (other.comparename, other.size)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.comparename, self.size) < \
               (other.comparename, other.size)
