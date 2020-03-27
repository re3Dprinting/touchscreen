import os

if __name__ == "__main__":
    input = "/usb/SAM_32"

    if os.path.islink(input):
        print("Is symbolic link")
        
        newpath = os.readlink(input)

        print("Path =", newpath)
