#!/bin/sh
sudo fbi -vt 1 -d /dev/fb0 -blend 1000 --noverbose /home/pi/service/re3d-logo.png
while :; do sleep 1; done
