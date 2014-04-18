import RPi.GPIO as GPIO
import sys, os, urllib2

button_pin_23 = 23
button_pin_24 = 24

pin_23_counter = 0
pin_24_counter =0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin_23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin_24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print ("button pin 23 and 24 (BCM GPIO)\n")

while True:
        if (GPIO.input(button_pin_23)):
            if(pin_23_counter==0):
                pin_23_counter=1
                try:
                    print urllib2.urlopen('http://192.168.0.106/test.php?arg1=xi&arg2=23').read()
                except OSError, e:
                    print "23 connection failed"
        elif (GPIO.input(button_pin_24)):
            if(pin_24_counter==0):
                pin_24_counter=1
                try:
                    print urllib2.urlopen('http://192.168.0.106/test.php?arg1=xi&arg2=24').read()
                except OSError, e:
                    print "24 connection failed"
        else:
            if(pin_23_counter > 0):
                pin_23_counter =0
                
            if(pin_24_counter > 0):
                pin_24_counter =0
