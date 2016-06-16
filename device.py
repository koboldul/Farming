import RPi.GPIO as io
import logging 

class DeviceTime:
	def __init__(self, start_hour, start_minute, stop_hour, stop_minute):
		self.start_hour = start_hour
		self.start_minute = start_minute
		self.stop_hour = stop_hour
		self.stop_minute = stop_minute
	
class Device:
	def __init__(self, pin, name, logger):
		self.pin = pin
		self.name = name
		self.logger = logger
		self.time_table = []

	def add_device_time(self, start_hour, start_minute, stop_hour, stop_minute):
			self.time_table.append(DeviceTime(start_hour, start_minute, stop_hour, stop_minute))
	
	def start_device(self):
		try:
			print self.name
			self.logger.info('Starting device ' + self.name + ' on pin ' + str(self.pin))
			io.setup(self.pin, io.OUT)
			io.output(self.pin, io.LOW)
			self.logger.info('Started ' + self.name + ' on pin ' + str(self.pin))
		except Exception as e:
			print str(e) 
			self.logger.info('Erro on ' + self.name + ' on pin ' + str(self.pin) + ' ERROR: ' + str(e))
			return False
		
		return True
	def stop_device(self):
		self.logger.info('Stopping device ' + self.name + ' on pin ' + str(self.pin))
		io.output(self.pin, io.HIGH)
		self.logger.info('Stopped device ' + self.name + ' on pin ' + str(self.pin))
	
