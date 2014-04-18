import RPi.GPIO as GPIO

button_pin_23 = 23
button_pin_24 = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin_23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin_24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print ("button pin 23 and 24 (BCM GPIO)\n")

while True:
        if (GPIO.input(button_pin_23)):
                print("pin 23 input")
        elif (GPIO.input(button_pin_24)):
                print("pin 24 input")
        # else:
                # print("no input")
