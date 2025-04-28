import RPi.GPIO as GPIO
import time

PIR_PIN = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Starting motion sensor test...")

try:
    while True:
        state = GPIO.input(PIR_PIN)
        print("Sensor state:", state)
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
