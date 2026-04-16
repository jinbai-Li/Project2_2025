import RPi.GPIO as GPIO
import time

# GPIO SETUP
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print("Water Detected!")
    else:
        print("Water Detected!")

# Let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300) 
# Assign function to GPIO PIN, Run function on change
GPIO.add_event_callback(channel, callback) 

# Infinite loop
try:
    while True:
        # Using sleep(1) instead of sleep(0) to prevent high CPU usage
        time.sleep(1)
except KeyboardInterrupt:
    # Clean up GPIO on CTRL+C exit
    GPIO.cleanup()

