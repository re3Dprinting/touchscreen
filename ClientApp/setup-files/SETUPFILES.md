Setup instructions for re3D touchscreen is posted [here](https://docs.google.com/document/d/1tEfo1iKyyIbEeY1O5UNwWr0Af3kb6Gi-DPLOItH8Gxw/edit?usp=sharing).

There are a total of three scripts that are ran to setup the re3d touchscreen.

setup-sys.sh

1. creates a interface between the raspberry pi and development machine (Is this necessary)
2. enable keyboard options (This option can be changed in raspi-config file)
3. change the password of the raspberry pi
4. sets up Wifi (Allow for inputing the wifi password manual)
5. Sets up ssh public keys (remove because not applicable to all users)

setup-sys2.sh

1. upgrade and update raspbian os system
2. relocate StartClientApp script to home directory
3. install global package dependencies for application.
   - git
   - python3-virtualenv
   - python3-pyqt5 : UI package for python
   - fbi : displays files on linux console using framebuffer device. jpeg, ppm, gif, png
   - emacs : file editor
   - lsof : report a list of all open files and processes that opened them.
   - xinit : program that allows user to manually start an X display server.
   - xserver-xorg : xorg is a display server, open source implementation of X Window System
   - x11-xserver-utils : toolbox for X server
   - x11-apps : miscellaneous X applications that ship with X Window System.
   - imagemagick : creating/modifying raster images
   - usbmount : mounts USB mass storage devices when plugged it.
4. Setup the scripts that configure the usbmount package that will mount filesystems when inserted.
5. Setup systemmd?
6. Create the usb directory that thumb drives will be mounted to.

setup-re3d.sh

1. create gcode/log cache, re3d dir, and copy over desktop background
2. Clone touchscreen and octoprint repo
3. create virtual environment and install octoprint/ touchscreen packages
4. create symbolic links for packages.
5. enable xinit services.
