# Ensure that we're running as root.
if [ `id -u` != 0 ]; then
    echo FATAL: Exected to be executed as root. Try using sudo.
    exit 1
fi

# Ensure that we're running from the setup-files directory, because
# that's the simplest way of knowing where the files are.
cd /home/pi/setup-files || (echo FATAL: Expected to find setup files in /home/pi/setup-files. ; exit 1)

#Enable ssh
systemctl enable ssh
systemctl start ssh

# Setup Locale
# https://www.jaredwolff.com/raspberry-pi-setting-your-locale/
perl -pi -e 's/# enUS.UTF-8 UTF-8/enUS.UTF-8 UTF-8/g' /etc/locale.gen
locale-gen enUS.UTF-8
update-locale enUS.UTF-8

# Setup Timezone
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
cp interface/shadow /etc/shadow
chown 640 /etc/shadow

# Copy wpa_supplicant over to boot folder
mkdir /boot/wpa_sup
cp interface/wpa_supplicant.conf /boot/wpa_sup

# Copy the inputRC file so we can ignore case on filename completion.
cp interface/dot-inputrc /home/pi/.inputrc

