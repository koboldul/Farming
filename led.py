import RPi.GPIO as GPIO
import logging
import logging.handlers
import time
import sys
import apscheduler

from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep

LOG_FILE ='farming.log'

#init stuff

GPIO.setmode(GPIO.BCM)

logger = logging.

pump = 17
valve = 4

lT = 3600

def startDevice(pin):
	global pump
	global valve
	p = 0
	if pin == 'v':
		p = valve
	if pin == 'p':
		p = pump
	if p == 0:
		p = pin
	print 'f - starting', p

	GPIO.setup(p,GPIO.OUT)
	GPIO.output(p, GPIO.LOW)
	
	print pin
	return
def checkIrrigation(pin):
	global valve
	return pin == 'v' or int(pin) == valve

hasIrrigation = False

if sys.argv[1] == 's':
	GPIO.setup(pump, GPIO.OUT)
	GPIO.setup(valve, GPIO.OUT)
	print 'stop'
	GPIO.cleanup()
else:
	try:
		for i in range(1,len(sys.argv)):
			print 'Starting', str(sys.argv[i])
			startDevice(sys.argv[i])
			if checkIrrigation(sys.argv[i]):
				hasIrrigation = True
				print 'Has irrigation'
			print 'Started', str(sys.argv[i])
		if hasIrrigation == True:
			time.sleep(slT)
			print 'Done with the irrigation'
			GPIO.setup(valve, GPIO.HIGH)
	except:
		print 'cleaning on error'
		kGPIO.cleanup()