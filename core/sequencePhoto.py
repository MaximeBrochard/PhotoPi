#!/usr/bin/env python

import config
from time import sleep
import datetime as dt
import os
import pygame
import os.path
import pygameEngine
import livePreview
import camera
import sys

def TakePictures():
	#Attribute a name with current time for all photos and composite
	photoFile = dt.datetime.now().strftime("%Y%m%d-%Hh%Mm%S")
	pic1 = TakeOnePicture("Smile :)", photoFile + "-1")
	pic2 = TakeOnePicture("~ Party ~", photoFile + "-2")
	pic3 = TakeOnePicture(".: More fun :.", photoFile + "-3")
	pic4 = TakeOnePicture("The last one :D", photoFile + "-4")
	Composite(pic1, pic2, pic3, pic4, photoFile)
	
def TakeOnePicture(message, photoFile):
    soundBeep1 = pygame.mixer.Sound(config.BEEP01_SOUND_FILE)
    soundBeep2 = pygame.mixer.Sound(config.BEEP02_SOUND_FILE)

    soundBeep1.play()
    pygameEngine.DrawCenterMessage("3", True)
    pygameEngine.DrawCenterMessage("2", True)
    pygameEngine.DrawCenterMessage("1", True)
    soundBeep2.play()
    pygameEngine.DrawCenterMessage(message, True)
    sleep(1)

    photoFile = config.SEQUENCE_PHOTO_CAPTURES + "/" + photoFile + ".jpg"
    if not os.path.isdir(config.SEQUENCE_PHOTO_CAPTURES) :
        os.makedirs(config.SEQUENCE_PHOTO_CAPTURES)

    camera.WaitCamera()
    pygameEngine.Fill(pygameEngine.WHITE_COLOR)
    camera.TakePhoto(photoFile)

    sleep(3)
    return photoFile

def Composite(pic1, pic2, pic3, pic4, photoFile):
    screen = pygameEngine.GetScreen()
    dtStart = dt.datetime.now()

    #Play sound
    waitSound = pygame.mixer.Sound(config.WAIT_SOUND_FILE)
    waitSound.play()

    #Create composite image 
    pygameEngine.WaitLogo()
    borderWidth = 20
    imageWidth = (config.WIDTH - 3 * borderWidth) / 2
    imageHeight = imageWidth * 2/3 #only work in landscape mode with 3/2 ratio
    borderHeight = (config.HEIGHT - 2 * imageHeight) / 3

    while os.path.exists(pic1) == False: # Wait for creation
        if dt.datetime.now() - dtStart * 24 * 60 > 1 : raise Exception('No image taken')  # special way out if no image appears
        sleep(.1)
    pbimage1 = pygame.image.load(pic1)
    pbimage1 = pygame.transform.scale(pbimage1, (imageWidth, imageHeight))

    while os.path.exists(pic2) == False: # Wait for creation
        sleep(.1)
    pbimage2 = pygame.image.load(pic2)
    pbimage2 = pygame.transform.scale(pbimage2, (imageWidth, imageHeight))

    while os.path.exists(pic3) == False: # Wait for creation
        sleep(.1)
    pbimage3 = pygame.image.load(pic3)
    pbimage3 = pygame.transform.scale(pbimage3, (imageWidth, imageHeight))

    while os.path.exists(pic4) == False: # Wait for creation
        sleep(.1)
    pbimage4 = pygame.image.load(pic4)
    pbimage4 = pygame.transform.scale(pbimage4, (imageWidth, imageHeight))

    i = 50
    while(i<=255):
        screen.fill(pygameEngine.WHITE_COLOR)
        pbimage1.set_alpha(i)
        pbimage2.set_alpha(i)
        pbimage3.set_alpha(i)
        pbimage4.set_alpha(i)
        screen.blit(pbimage1, (borderWidth, borderHeight))
        screen.blit(pbimage2, (2 * borderWidth + imageWidth, borderHeight))
        screen.blit(pbimage3, (borderWidth, 2 * borderHeight + imageHeight))
        screen.blit(pbimage4, (2 * borderWidth + imageWidth, 2 * borderHeight + imageHeight))
        pygame.display.flip()
        #pygame.time.delay(5) #To slow down animation
        i += 5 #To speed up animation

    if not os.path.isdir(config.SEQUENCE_PHOTO_COMPOSITES) :
        os.makedirs(config.SEQUENCE_PHOTO_COMPOSITES)
    pygame.image.save(screen, config.SEQUENCE_PHOTO_COMPOSITES + "/" + photoFile + ".jpg")
    sleep(10)

def Start():
    try:
        print "Photo Start"
        livePreview.Start()
        TakePictures()
    except Exception, e:
        print "ERREUR : Photo : " + str(sys.exc_info()[0]) + " : " + str(e)
        pygameEngine.ShowError()