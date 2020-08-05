git clone https://github.com/re3Dprinting/touchscreen.git --branch feature/octo-integration
git clone https://github.com/jim-thompson/OctoPrint.git --branch devel OctoPrint
ln -s OctoPrint OctoPrint-1.4.0rc3
cd OctoPrint
python3 -m virtualenv --system-site-packages ./venv
. venv/bin/activate
pip install --upgrade pip
pip install gitpython
pip install rpi-backlight
echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules

pip install -e .[develop,plugins]
mkdir localgcode
