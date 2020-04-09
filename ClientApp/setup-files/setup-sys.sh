# Ensure that we're running as root.
if [ `id -u` != 0 ]; then
    echo FATAL: Exected to be executed as root. Try using sudo.
    exit 1
fi

# Ensure that we're running from the setup-files directory, because
# that's the simplest way of knowing where the files are.
cd /home/pi/setup-files || (echo FATAL: Expected to find setup files in /home/pi/setup-files. ; exit 1)

# Copy the hosts file. This establishes some host names, in particular
# 'mac', which we can find at the other end of ethernet interface. (We
# expect to route to the Internet through the wi-fi interface; the
# ethernet interface is for debug/diagnostic support.)
#
#     raspberrypi (10.0.1.2) <-----> mac (10.0.1.1)
#
cp hosts /etc/hosts

# Copy the interfaces file. This defines the IP address for the 'eth0'
# interface (ethernet); and establishes that as the 10.0.1/24 network.
cp interfaces /etc/network/interfaces

# Copy the keyboard default file. This ensures we have a US keyboard
# layout (the default for Raspbian is UK layout). It also maps the
# CAPS LOCK key to be another control key and (optionally) sets the
# keyboard variant to Dvorak (for Jim's CTS).
cp keyboard /etc/default/keyboard

# Copy the passwd and shadow files. This is a simple way of ensuring
# that the 'pi' user password is what we want it to be, without having
# to enter its plaintext into a setup file.
cp shadow /etc/shadow
chown 640 /etc/shadow

# Copy the WPA supplicant file. This sets the wi-fi SSIDs and
# passwords for the networks we wish to configure out of the
# box. (Future versions will enable custom configurations of wi-fi
# networks.
cp wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf

# Run the remainder of the script as user 'pi':
su pi << EOF

# Set up the SSH configuration, including public keys (for fast access
via SSH without having to enter a password every time).

mkdir -p /home/pi/.ssh
cp id_rsa.pub /home/pi/.ssh/id_rsa.pub
cp authorized_keys /home/pi/.ssh/authorized_keys

# Ensure the SSH files have the right ownership and mode, or the SSH
programs will ignore them.

chown pi:pi /home/pi/.ssh
chown pi:pi /home/pi/.ssh/id_rsa.pub
chown pi:pi /home/pi/.ssh/authorized_keys

# Copy the inputRC file so we can ignore case on filename completion.
cp dot-inputrc /home/pi/.inputrc

EOF
