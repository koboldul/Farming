import RPi.GPIO as GPIO
import time
import sys
import apscheduler
import datetime
import util
from device import Device
from mailer import Mailer
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep

LOG_FILE ='farming.log'

#init stuff

GPIO.setmode(GPIO.BCM)

logger = util.get_logger(LOG_FILE)
mailer = Mailer()

pump = Device(17, 'pump', logger)
valve = Device(4, 'irrigation valve', logger)
sprinkler1 = Device(1, 'sprinkler front house', logger)

pump.add_device_time(9,0,18,30)
pump.add_device_time(22,0,4,0)
valve.add_device_time(6,30,7,0)
valve.add_device_time(21,30,22,00)

rainDetectedAt = None

def add_to_scheduler(scheduler, device):
	for dTime in device.time_table:
			scheduler.add_job(lambda: device.start_device(), 'cron', hour=dTime.start_hour, minute=dTime.start_minute, misfire_grace_time=None)
			scheduler.add_job(lambda: device.stop_device(), 'cron', hour=dTime.stop_hour, minute=dTime.stop_minute, misfire_grace_time=None)
try:		
	#daemon mode
	scheduler = BackgroundScheduler()
	
	add_to_scheduler(scheduler, pump)
	add_to_scheduler(scheduler, valve)
	scheduler.start()
	logger.info('Starting app..')
except Exception as e:
	logger.info('Error {0}'.format(str(e)))

try:
	while(True):
		time.sleep(3600)
		logger.info('still awake..')
		i = 1
		if i == 0:
			rainDetectedAt = datetime.now()
finally:
	scheduler.shutdown()
	logger.info('Shutting down all stop')
	print 'stopping all'
	GPIO.cleanup()
	mailer.sendFullStopMessage()
