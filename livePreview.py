#!/usr/bin/env python

import os
import os.path
import pygameEngine

# Variables
liveMovie = "fifo.mjpg"
previewDuration = 10 #secondes

def Start():
	# Start recording live preview
	pygameEngine.DrawCenterMessage("Prepare for fun",True)
	print "Start recording live preview"
	if os.path.exists(liveMovie):
		os.remove(liveMovie)
	os.mkfifo(liveMovie)
	os.popen("gphoto2 --capture-movie=" + str(previewDuration) + "s --stdout> " + liveMovie + " &")

	# Playing live preview
	pygameEngine.DrawCenterMessage("") #Clean screen before preview
	print "Playing live preview"
	os.popen("omxplayer " + liveMovie + " --live")
	
	#Deleting live preview
	os.remove(liveMovie)