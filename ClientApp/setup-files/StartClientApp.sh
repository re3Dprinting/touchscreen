#! /bin/sh

# This script will be executed as user 'root'; switch to user 'pi'
# before executing anything.
sudo su - pi << EOF

# Set environment variables to point to the default X server.

export DISPLAY=:0

# Do we need these still?

export XAUTHORITY=/home/pi/.Xauthority
export XDG_RUNTIME_DIR=/run/user/1000

# Change into the OctoPrint directory; everything runs best from
# here.

cd /home/pi/re3d/OctoPrint

# Source the activate file to set up the virtual environment.

. venv/bin/activate

# Turn off the X screen saver. Here's why we have to do this: when the
# screen saver activates, the display goes dark and a user will have
# to touch the screen to make the UI visible again. However, that
# touch event WILL get passed to the UI. This can cause trouble if,
# for example, the user happens to touch a button or slider. It's
# easiest to fix this by just turning off the screen saver. However,
# this is not a good long-term solution, because leaving the
# screensave off can lead to screen burn-in.

xset s off
xset -dpms

# Loop forever (so that if the UI dies or exits, it will be
# automatically restarted.

while :; do
    # Add a startup message to the script log (Note: this is not the
    # same as the python log, which is in ts.log*

    echo "Touchscreen starting..." >> touchscreen.out
    date >> touchscreen.out

    # Run the UI. Redirect all output, including stderr, to the script
    # log.

    python src/touchscreen/main.py >> touchscreen.out 2>&1
done

EOF
