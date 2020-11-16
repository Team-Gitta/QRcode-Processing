#!/bin/bash
DATE='image'

fswebcam -r 1280x720 --no-banner /home/pi/gitta/QRcode-Processing/capture/$DATE.jpg

python3 qrcodeReader.py --filename capture/${DATE}.jpg

