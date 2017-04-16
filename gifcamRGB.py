import picamera, time, os, random, string, datetime
from time import sleep
import RPi.GPIO as GPIO
from os import system
from multiprocessing import Process

p = None

shutterbutton = 19
statusled_b = 16
statusled_g =20
statusled_r = 21
powerled = 12       #on shutter button

numpics = 8
gifdelay = 15 #ms

freq = 100
statusR = None
statusG = None
statusB = None

gifdirectory = '/home/pi/gifs/'

camera = picamera.PiCamera()

#TODO: check switches. bottommost is power, doesn't matter in code
#      uppermost is camera/wifi. if camera, turn off wifi, turn on camera
#      if wifi, turn off camera, turn on wifi (flask should always be running)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(shutterbutton, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(powerled, GPIO.OUT)
    GPIO.setup(statusled_b, GPIO.OUT)
    GPIO.setup(statusled_g, GPIO.OUT)
    GPIO.setup(statusled_r, GPIO.OUT)
    

    ######
    # PiCam settings
    ######
    camera.ISO = 400    
    camera.resolution = (800,800)
    camera.rotation = 0            #TODO: make sure this is correct
    #camera.sharpness = 0
    #camera.contrast = 50
    #camera.brightness = 80
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

    GPIO.output(powerled, 1)

    statusR = GPIO.PWM(statusled_r, freq)
    statusG = GPIO.PWM(statusled_g, freq)
    statusB = GPIO.PWM(statusled_b, freq)
    statusR.start(0)
    statusG.start(0)
    statusB.start(0)
    

def statusLED(R,G,B):
    while True:
        for i in range(0,101):
            statusR.ChangeDutyCycle(R*i)
            statusG.ChangeDutyCycle(G*i)
            statusB.ChangeDutyCycle(B*i)
            sleep(0.02)
        for i in range(101,0):
            statusR.ChangeDutyCycle(R*i)
            statusG.ChangeDutyCycle(G*i)
            statusB.ChangeDutyCycle(B*i)
            sleep(0.02)
        
    
    

#TODO: define function to switch on wireless and start flask/something to serve up gifs

if __name__ == "__main__":
    setup()

    p = Process(target=statusLED, args=(0,0,255,))
    p.start()
    p.join()

    try:
        while True:
            shutter = GPIO.input(shutterbutton)
            if p.pid != None:
                p.terminate()
            p = Process(target=statusLED, args=(0,255,0,))
            p.start()
            p.join()
            if shutter == False:
                p.terminate()
                p = Process(target=statusLED, args=(255,255,0,))
                p.start()
                p.join()
                print('Giffing')
                for i in range(numpics):
                    camera.capture('image{0:04d}.jpg'.format(i))
                filename = gifdirectory + datetime.datetime.now().strftime("%Y-%m-%d%H%M%S") + ".gif"
                print('combining')
                magick = "gm convert -delay " + str(gifdelay) + " *.jpg " + filename
                os.system(magick)
                print('magicked\nready')
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()
