# Ensure that we're running as root.
if [ `id -u` != 0 ]; then
    echo FATAL: Exected to be executed as root. Try using sudo.
    exit 1
fi

# Ensure that we're running from the setup-files directory, because
# that's the simplest way of knowing where the files are.
cd /home/pi/setup-files || (echo FATAL: Expected to find setup files in /home/pi/setup-files. ; exit 1)

su pi << EOF

# Make the directories that will contain local copies of the GCode
# files.
mkdir -p /home/pi/gcode-cache
mkdir -p /home/pi/log-cache

# Copy the PNG file that we use as the desktop background.
cp re3d-logo.png /home/pi/desktop-background
mkdir -p /home/pi/re3d

# Change to the directory that will contain the OctoPrint and
# touchscreen executable code.
cd /home/pi/re3d

# Clone the touchscreen and OctoPrint source repositories
git clone https://github.com/re3Dprinting/touchscreen.git
git clone https://github.com/jim-thompson/OctoPrint.git --branch devel OctoPrint

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

# Make same symbolic links to make Python happy. The first is for the
# icon files we use in the UI. The second is for the touchscreen
# source code.
ln -s ../touchscreen/ClientApp/img .
ln -s ../../touchscreen/ClientApp ./src/touchscreen

EOF

# Enable the Xinit service.
cp xinit.service /etc/systemd/system/
systemctl enable xinit
