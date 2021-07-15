#!/bin/bash
DIR="/home/pi/photobooth/PhotoPi/captures/photo-captures"
inotifywait -r -m -e create "$DIR" | while read f

do
	cp $f /media/usb
done
