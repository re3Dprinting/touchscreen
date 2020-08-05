# Ensure that we're running as root.
if [ `id -u` != 0 ]; then
    echo FATAL: Exected to be executed as root. Try using sudo.
    exit 1
fi

# Ensure that we're running from the setup-files directory, because
# that's the simplest way of knowing where the files are.
cd /home/pi/setup-files || (echo FATAL: Expected to find setup files in /home/pi/setup-files. ; exit 1)

# Update Raspbian
apt-get upgrade
apt-get update -y

# Install OS packages that we require.
apt-get install git python3-virtualenv python3-pyqt5 python3-pyqt5.qtquick qml-module-qtquick2 qtquickcontrols5-* fbi lsof xinit xserver-xorg x11-xserver-utils x11-apps usbmount --fix-missing -y

# Set up the scripts that configure the 'usbmount' package, which will
# mount any recognized filesystem when a USB thumb drive is inserted.
cp usb/usbmount.conf /etc/usbmount/usbmount.conf
cp usb/00_create_model_symlink /etc/usbmount/mount.d/
cp usb/00_remove_model_symlink /etc/usbmount/umount.d/

chown root:root /etc/usbmount/mount.d/00_create_model_symlink
chown root:root /etc/usbmount/umount.d/00_remove_model_symlink 

chown 755 /etc/usbmount/mount.d/00_create_model_symlink
chmod 755 /etc/usbmount/umount.d/00_remove_model_symlink
chmod 644 /etc/usbmount/usbmount.conf

#Set PrivateMount to No in systemd-udevd.service
cp usb/systemd-udevd.service /lib/systemd/system/systemd-udevd.service
chmod 644 /lib/systemd/system/systemd-udevd.service

# Make the directory we're going to use to contain symbolic links to
# mounted thumb drives.
mkdir /usb
chown root:root /usb