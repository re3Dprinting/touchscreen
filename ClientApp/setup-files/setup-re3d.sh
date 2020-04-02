if [ `id -u` != 0 ]; then
    echo FATAL: Exected to be executed as root. Try using sudo.
    exit 1
fi
cd /home/pi/setup-files || (echo FATAL: Expected to find setup files in /home/pi/setup-files. ; exit 1)

su pi << EOF

mkdir -p /home/pi/gcode-cache
mkdir -p /home/pi/log-cache

cp re3d-logo.png /home/pi/desktop-background
mkdir -p /home/pi/re3d

cd /home/pi/re3d

git clone https://github.com/re3Dprinting/touchscreen.git
git clone https://github.com/jim-thompson/OctoPrint.git --branch devel OctoPrint

cd OctoPrint

python3 -m virtualenv -p /usr/bin/python3 --system-site-packages ./venv
. venv/bin/activate

pip install --upgrade pip
pip install -e .[develop,plugins]
pip install gitpython

ln -s ../touchscreen/ClientApp/img .
ln -s ../../touchscreen/ClientApp ./src/touchscreen

EOF

cp xinit.service /etc/systemd/system/
systemctl enable xinit
