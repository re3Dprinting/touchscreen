#! /bin/sh
sudo su - pi << EOF
export DISPLAY=:0
export XAUTHORITY=/home/pi/.Xauthority
export XDG_RUNTIME_DIR=/run/user/1000

cd /home/pi/re3d/OctoPrint
. venv/bin/activate
xset s off
xset -dpms
while :; do
    echo "Touchscreen starting..." >> touchscreen.out
    date >> touchscreen.out
    python src/touchscreen/main.py >> touchscreen.out 2>&1
done
EOF
