#!/bin/bash
dir=/home/pi/photobooth/PhotoPi/captures/photo-captures/
target=/media/usb/

inotifywait -m "$dir" --format '%w%f' -e close_write |
	while read file; do
		#echo "$file" 
		cp "$file" "$target"
	done
