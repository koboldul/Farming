import RPi.GPIO as GPIO
import logging
import logging.handlers
import time
import sys
import apscheduler
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep

LOG_FILE ='farming.log'

#init stuff

GPIO.setmode(GPIO.BCM)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

pump = 17
valve = 4

rainDetectedAt = None

pumpTime = 24000
valveTime = 5000

def startDevice(pin):
	global pump
	global valve
	p = pin
	if pin == 'v':
		p = valve
	if pin == 'p':
		p = pump
	logger.info('Starting device ' + str(p))
	try:
		GPIO.setup(p,GPIO.OUT)
		GPIO.output(p, GPIO.LOW)
		logger.info('Started device ' + str(p))
	except Exception as e:
		logger.info('Error starting device ' + str(p) + ' ERROR: ' + str(e))
		print e

	return

def checkIrrigation(pin):
	global valve
	try:
		return pin == 'v' or int(pin) == valve
	except:
		return False

def stopDevice(pin):
	logger.info("Stopping device " + str(pin))
	GPIO.output(pin, GPIO.HIGH)
	logger.info("Stoped device " + str(pin))

if len(sys.argv) == 0:
	print 'Daemon mode'
	scheduler = BackgroundScheduler()
	scheduler.add_job(lambda: startDevice(pump),'cron', hour='8,22', minute=0)
	scheduler.add_job(lambda: startDevice(valve),'cron', hour='6,20', minute=0)
	scheduler.add_job(lambda: stopDevice(pump), 'cron', hour='16,2', minute=0)
	scheduler.add_job(lambda: stopDevice(valve), 'cron', hour='7,21', minute=0)
	scheduler.start()
	while(True):
		i = 1
		if i == 0:
			rainDetectedAt = datetime.now()

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
			time.sleep(valveTime)
			print 'Done with the irrigation'
			GPIO.setup(valve, GPIO.HIGH)
	except Exception as e:
		print e
		logger.info(e)
		print 'cleaning on error'
		GPIO.cleanup()
