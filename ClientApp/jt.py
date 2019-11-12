from fsutils.subfilesystem import *

if __name__ == "__main__":

    it = SubFileSystem("/Users/jct")
    files = it.list()

    for file_tuple in files:
        if (file_tuple.type == 'f'):
            print(file_tuple.displayname, file_tuple.size)
        else:
            print(file_tuple.displayname)
