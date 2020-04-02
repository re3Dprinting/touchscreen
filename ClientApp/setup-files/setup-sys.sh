if [ `id -u` != 0 ]; then
    echo FATAL: Exected to be executed as root. Try using sudo.
    exit 1
fi
cd /home/pi/setup-files || (echo FATAL: Expected to find setup files in /home/pi/setup-files. ; exit 1)

cp hosts /etc/hosts
cp interfaces /etc/network/interfaces
#cp keyboard /etc/default/keyboard
cp shadow /etc/shadow
chown 640 /etc/shadow
cp wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
su pi << EOF
mkdir -p /home/pi/.ssh
cp id_rsa.pub /home/pi/.ssh/id_rsa.pub
cp authorized_keys /home/pi/.ssh/authorized_keys
chown pi:pi /home/pi/.ssh
chown pi:pi /home/pi/.ssh/id_rsa.pub
chown pi:pi /home/pi/.ssh/authorized_keys
cp dot-inputrc /home/pi/.inputrc
EOF
