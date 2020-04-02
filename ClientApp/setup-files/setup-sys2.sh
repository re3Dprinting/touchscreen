if [ `id -u` != 0 ]; then
    echo FATAL: Exected to be executed as root. Try using sudo.
    exit 1
fi
cd /home/pi/setup-files || (echo FATAL: Expected to find setup files in /home/pi/setup-files. ; exit 1)

apt-get upgrade
apt-get update -y

mkdir -p /media/pi

cp StartClientApp.sh /home/pi/StartClientApp.sh
chmod +x /home/pi/StartClientApp.sh

apt-get install git python3-virtualenv python3-pyqt5 fbi emacs lsof xinit xserver-xorg x11-xserver-utils x11-apps imagemagick usbmount --fix-missing -y

cp 00_create_model_symlink /etc/usbmount/mount.d/
cp 00_remove_model_symlink /etc/usbmount/umount.d/

chown root:root /etc/usbmount/mount.d/00_create_model_symlink
chown root:root /etc/usbmount/umount.d/00_remove_model_symlink 

chown 755 /etc/usbmount/mount.d/00_create_model_symlink
chmod 755 /etc/usbmount/umount.d/00_remove_model_symlink 

cp systemd-udevd.service /lib/systemd/system/systemd-udevd.service
chmod 644 /lib/systemd/system/systemd-udevd.service

mkdir /usb
chown root:root /usb

