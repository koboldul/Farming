import RPi.GPIO as GPIO
import time
import sys
import apscheduler
import datetime
import util
from device import Device
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep

LOG_FILE ='farming.log'

#init stuff

GPIO.setmode(GPIO.BCM)

logger = util.get_logger(LOG_FILE)

pump = Device(17, 'pump', logger)
valve = Device(4, 'irrigation valve', logger)
sprinkler1 = Device(1, 'sprinkler front house', logger)

pump.add_device_time(10,0,18,0)
pump.add_device_time(22,0,1,0)
valve.add_device_time(6,30,7,0)
valve.add_device_time(21,30,22,00)

rainDetectedAt = None

def add_to_scheduler(scheduler, device):
	for dTime in device.time_table:
			scheduler.add_job(lambda: device.start_device(), 'cron', hour=dTime.start_hour, minute=dTime.start_minute, misfire_grace_time=None)
			scheduler.add_job(lambda: device.stop_device(), 'cron', hour=dTime.stop_hour, minute=dTime.stop_minute, misfire_grace_time=None)
		
#daemon mode
if len(sys.argv) == 1:
	print 'Daemon mode'
	scheduler = BackgroundScheduler()
	
	add_to_scheduler(scheduler, pump)
	add_to_scheduler(scheduler, valve)

	scheduler.start()
	try:
		while(True):
			time.sleep(3600)
			logger.info('still awake..')
			i = 1
			if i == 0:
				rainDetectedAt = datetime.now()
	finally:
		scheduler.shutdown()
		print 'stopping all'
		GPIO.cleanup()
#command line mode
valveTime = 5000
if sys.argv[1] == 's':
	GPIO.setup(pump, GPIO.OUT)
	GPIO.setup(valve, GPIO.OUT)
	print 'stop'
	GPIO.cleanup()
else:
	try:
		for i in range(1,len(sys.argv)):
			print 'Starting', str(sys.argv[i])
			if sys.argv[i] == 'p':
				pump.start_device()
				print 'Started ', str(sys.argv[i])
			if sys.argv[i] == 'v':
				valve.start_device()
				print 'Started ', str(sys.argv[i])
				time.sleep(valveTime)
				print 'Done with the irrigation'
				valve.stop_device()
	except Exception as e:
		print e
		logger.info(e)
		print 'cleaning on error'
		GPIO.cleanup()
