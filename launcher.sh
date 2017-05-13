#!/bin/sh

# change to appropriate file containing python flask page
export FLASK_APP=webpages.py
# runs flask as an externally visible server
# only serves up images so we (shouldn't) need a seperate server program running too
python -m flask run --host=0.0.0.0
sudo ifdown wlan0
sudo service hostapd start
sudo ifup wlan0=adhoc

# actual program responsible for take pictures and making gifs
# change back to gifcam.py for Nick Brewer's original Pix-E program
sudo python gifcamRGB.py