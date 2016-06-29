import RPi.GPIO as GPIO
import sys
import apscheduler
import datetime

from notifier import Notifier
from device import Device
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
from weather_report_current import WeatherReportCurrent
from weather_report_historical import WeatherReportHistorical

#init stuff

GPIO.setmode(GPIO.BCM)

_notifier = Notifier()
_currentWeatherReporter = WeatherReportCurrent(None, _notifier)
_weatherReporter = WeatherReportHistorical(_currentWeatherReporter, _notifier)

pump = Device(17, 'pump', _notifier)
valve = Device(4, 'irrigation valve', _notifier, weather_dependent=True)
sprinkler1 = Device(1, 'sprinkler front house', _notifier, weather_dependent=True)

pump.add_device_time(9,0,18,30)
pump.add_device_time(22,0,4,0)
valve.add_device_time(7,0,7,30)
valve.add_device_time(21,30,22,00)

rainedAt = []
#utility functions
def shift(seq, el):
	idx = [i for i, v in enumerate(seq) if v is not None]
	
	if el is not None:
		idx = idx[len(idx)-1]+1 if len(idx) > 0 else 0
	else:
		idx = idx[len(idx)-1] if len(idx) > 0 else 0
	if idx < len(seq):
		seq[idx] = el
        	return seq
	else:
		return seq[(-len(seq)+1):] + [el]

def start_device(device):
    global rainedAt
    
    if device.weather_dependent:
		waterDecision = w_currentWeatherReporter.get_watering_response(rainedAt)
		if waterDecision.should_water:
			device.start_device()
		else:
			_notifier.notify('Skip watering for {0} because of the rainy weather'.format(device.name), 'Watering skipped')
    else:
		device.start_device()

def add_to_scheduler(scheduler, device):
	for dTime in device.time_table:
			scheduler.add_job(lambda: start_device(device), 'cron', hour=dTime.start_hour, minute=dTime.start_minute, misfire_grace_time=None)
			scheduler.add_job(lambda: device.stop_device(), 'cron', hour=dTime.stop_hour, minute=dTime.stop_minute, misfire_grace_time=None)

try:		
	#daemon mode
	scheduler = BackgroundScheduler()
	
	add_to_scheduler(scheduler, pump)
	add_to_scheduler(scheduler, valve)

	scheduler.start()
	_notifier.log('Starting app..')
except Exception as e:
	_notifier.notify('Error {0}'.format(str(e)), "Error scheduling things")

try:
	while(True):
		sleep(30)
		waterDecision = _currentWeatherReporter.get_watering_response([])
		if waterDecision.rainedAt is not None:
			_notifier.log('Rained at {0}'.format(waterDecision.rainedAt)
		rainedAt = shift(rainedAt, waterDecision.rainedAt)

finally:
	scheduler.shutdown()
	_notifier.notify('Shutting down all stop', 'App stopped')
	GPIO.cleanup()
