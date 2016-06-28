import RPi.GPIO as io
import logging 

class DeviceTime:
	def __init__(self, start_hour, start_minute, stop_hour, stop_minute):
		self.start_hour = start_hour
		self.start_minute = start_minute
		self.stop_hour = stop_hour
		self.stop_minute = stop_minute
	
class Device:
	def __init__(self, pin, name, logger, weather_dependent=False):
		self.weather_dependent = weather_dependent
		self.pin = pin
		self.name = name
		self.logger = logger
		self.time_table = []

	def add_device_time(self, start_hour, start_minute, stop_hour, stop_minute):
			self.time_table.append(DeviceTime(start_hour, start_minute, stop_hour, stop_minute))
	
	def start_device(self):
		try:
			self.logger.log('Starting device ' + self.name + ' on pin ' + str(self.pin))
			io.setup(self.pin, io.OUT)
			io.output(self.pin, io.LOW)
			self.logger.notify('Started ' + self.name + ' on pin ' + str(self.pin), 'Device {0} started'.format(self.name))
		except Exception as e:
			self.logger.notify('Error on starting ' + self.name + ' on pin ' + str(self.pin) + ' ERROR: ' + str(e), \
                'Error')
			return False
		
		return True
	def stop_device(self):
		self.logger.log('Stopping device ' + self.name + ' on pin ' + str(self.pin))
		io.setup(self.pin, io.OUT)
		io.output(self.pin, io.HIGH)
		self.logger.notify('Stopped device ' + self.name + ' on pin ' + str(self.pin), 'Device {0} stopped'.format(self.name))
		
			
		
	
