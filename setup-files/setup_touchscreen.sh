#!/bin/bash

programname=$0
function usage {
    echo "usage: $programname [-c <type>]"
    echo "  -c <type> setup touchscreen application as <type>"
    echo " <type>     <type> can be the follow: \"developer\", \"beta-tester\", \"customer\" (default is \"customer\")"
    exit 1
}

declare -a versions=("developer" "beta-tester" "customer")
if [[ $# -ne 0 && $# -ne 2 ]]; then
    echo "Invalid number of arguments"
    exit 1
fi

software_version="customer"
if [[ $# -eq 2 ]]; then
    if [[ $1 == '-c' ]]; then
        if [[ " ${versions[@]} " =~ " $2 " ]]; then
            software_version=$2
            echo "Setting to $2 software version"
        else
            echo "Invalid argument \"$2\""
            exit 1
        fi
    else
        echo "Invalid argument \"$1\""
        exit 1
    fi
else
    echo "Defaulting to customer software version"
fi

# Ensure that we're running as root.
if [ `id -u` != 0 ]; then
    echo FATAL: Exected to be executed as root. Try using sudo.
    exit 1
fi


# Ensure that we're running from the setup-files directory, because
# that's the simplest way of knowing where the files are.
cd /home/pi/setup-files || (echo FATAL: Expected to find setup files in /home/pi/setup-files. ; exit 1)

#Enable ssh
echo "Enabling ssh..."
systemctl enable ssh
systemctl start ssh

# Setup Locale
# https://www.jaredwolff.com/raspberry-pi-setting-your-locale/
echo "Adjusting Locale..."
perl -pi -e 's/# enUS.UTF-8 UTF-8/enUS.UTF-8 UTF-8/g' /etc/locale.gen
locale-gen enUS.UTF-8
update-locale enUS.UTF-8

# Setup Timezone
echo "Settingup timezone..."
timedatectl set-timezone America/Mexico_City

# Copy the hosts file. This establishes some host names, in particular
# 'mac', which we can find at the other end of ethernet interface. (We
# expect to route to the Internet through the wi-fi interface; the
# ethernet interface is for debug/diagnostic support.)
#
#     raspberrypi (10.0.1.2) <-----> mac (10.0.1.1)
#
cp interface/hosts /etc/hosts
# Copy the interfaces file. This defines the IP address for the 'eth0'
# interface (ethernet); and establishes that as the 10.0.1/24 network.
cp interface/interfaces /etc/network/interfaces

# Copy the keyboard default file. This ensures we have a US keyboard
# layout (the default for Raspbian is UK layout). 
cp interface/keyboard /etc/default/keyboard

# Copy the passwd and shadow files. This is a simple way of ensuring
# that the 'pi' user password is what we want it to be, without having
# to enter its plaintext into a setup file.
echo "Copying over password file..."
cp interface/shadow /etc/shadow
chown 640 /etc/shadow

# Copy the inputRC file so we can ignore case on filename completion.
echo "Copying .inputrc file..."
cp interface/dot-inputrc /home/pi/.inputrc

# Copy wpa_supplicant over to boot folder
mkdir /boot/wpa_sup
cp interface/wpa_supplicant.conf /boot/wpa_sup

# Copy wpa supplicant file over to etc folder and reload Wifi
echo "Copying wpa_supplicant.conf"
cp interface/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
rfkill unblock wifi
rfkill unblock all

echo "Restarting Wifi... "
wpa_cli -i wlan0 reconfigure
sudo systemctl daemon-reload
sudo systemctl restart wpa_supplicant

echo "Trying to sleep for 15 seconds"
sleep 15

echo "Pinging to check for Internet Connection"
if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
  echo "IPv4 is up"
else
  echo "IPv4 is down please edit /etc/wpa_supplicant/wpa_supplicant.conf"
  exit 1
fi

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


#RE3D FILE SETUP
su pi << EOF

# Make the directories that will contain local copies of the GCode
# files.
mkdir -p /home/pi/gcode-cache
mkdir -p /home/pi/log-cache
mkdir -p /home/pi/re3d

# Change to the directory that will contain the OctoPrint and
# touchscreen executable code.
cd /home/pi/re3d

# Clone the touchscreen and OctoPrint source repositories
git clone https://github.com/re3Dprinting/touchscreen.git
git clone https://github.com/jim-thompson/OctoPrint.git --branch devel OctoPrint

cd touchscreen
git checkout beta/1.0.0
cd ..

# Change into the directory for OctoPrint. We'll run everything from
# this directory.
cd OctoPrint

# Set up the virtual environment we'll use to execute Python for the
# touchscreen.
python3 -m virtualenv -p /usr/bin/python3 --system-site-packages ./venv

# Activate the virtual enverinment.
. venv/bin/activate

# Install the packages required by OctoPrint.
pip install --upgrade pip
pip install -e .[develop,plugins]

# Install the packages required by the touchscreen.
pip install gitpython
pip install rpi-backlight

EOF

echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules

# Copy config.properties over to re3d directory
cp /home/pi/setup-files/config.properties /home/pi/re3d/
sed -i "s/customer/$software_version/g" /home/pi/re3d/config.properties
chmod 777 /home/pi/re3d/config.properties

# Make starting script executable
chmod +x /home/pi/re3d/touchscreen/StartTouchscreen.sh

# Enable the Xinit service.
cp xinit.service /etc/systemd/system/
systemctl enable xinit

# Enable Splahscreen through service.
echo "disable_splash=1" >> /boot/config.txt
sed -i 's/tty1/tty3/g' /boot/cmdline.txt
truncate -s -1 /boot/cmdline.txt 
echo -n ' logo.nologo vt.global_cursor_default=0 consoleblank=0 loglevel=1 quiet' >> /boot/cmdline.txt

ln -s /home/pi/re3d/touchscreen/boot/splashscreen.service /etc/systemd/system/splashscreen.service
systemctl enable splashscreen

reboot