import picamera
from time import sleep
import time
import RPi.GPIO as GPIO
from os import system
import os
import random, string

shutterbutton = 19
statusled = 12
powerled = 21

numpics = 8
gifdelay = 15 #ms

gifdirectory = '/home/pi/gifcam/gifs/'

camera = picamera.PiCamera()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(shutterbutton, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(statusled, GPIO.OUT)
    GPIO.setup(powerled, GPIO.OUT)

    ######
    # PiCam settings
    ######
    camera.ISO = 400    
    camera.resolution = (800,800)
    camera.rotation = 90            #TODO: make sure this is correct
    #camera.sharpness = 0
    camera.contrast = 50
    camera.brightness = 80
    #camera.saturation = 0
    camera.image_effect = 'none'
    #camera.video_stabilization = False
    #camera.exposure_compensation = 0
    #camera.exposure_mode = 'auto'
    #camera.meter_mode = 'average'
    #camera.awb_mode = 'auto'
    #camera.color_effects = (128,128)
    #camera.hflip = False
    #camera.vflip = False
    #camera.crop = (0.0, 0.0, 1.0, 1.0)

    GPIO.output(statusled, 1)

#TODO: define function to switch on wireless and start flask/something to serve up gifs

def main():
    setup()

    while True:
        shutter = GPIO.input(shutterbutton)
        if shutter == False:
            GPIO.output(statusled, 1)
            print('Giffing')
            for i in range(numpics):
                camera.capture('image{0:04d}.jpg'.format(i))
            filename = gifdirectory + datetime.datetime.now().strftime("%Y-%m-%d%H%M%S") + ".gif"
            print('combining')
            magick = "gm convert -delay " + str(gifdelay) + " *.jpg " + filename
            os.system(magick)
            print('magicked\nready')
        else:
            GPIO.output(statusled, 1)
            time.sleep(0.35)
            GPIO.output(statusled, 0)
            time.sleep(0.35)
main()
