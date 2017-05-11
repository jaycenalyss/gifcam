#!/bin/bash
sudo ifdown wlan0
sudo ifup wlan0=adhoc
sudo service hostapd start
python -m flask run --host=0.0.0.0