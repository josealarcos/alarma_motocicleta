import RPi.GPIO as GPIO
import time
from datetime import datetime as dt

def alarma(num):
	pin=21
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)
	for i in range(2*num):
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(pin, GPIO.LOW)
		time.sleep(0.5)

def activar(num):
	pin=21
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)
	for i in range(num):
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(0.2)
		GPIO.output(pin, GPIO.LOW)
		time.sleep(0.1)

#-----------------------------
#alarma(2)

