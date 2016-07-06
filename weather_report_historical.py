import json
import requests
import datetime
from weather_report_base import WeatherReportBase
from private_data import PrivateData
from watering_response import WateringResponse

class WeatherReportHistorical(WeatherReportBase):
	def __init__(self, successor, logger):
        	super(WeatherReportHistorical, self).__init__(successor, logger)

	def can_handle(self, input):
        	return len(input) > 0

	def handle_query(self, input):
		resp = WateringResponse()
		try:
			idx = [i for i, v in enumerate(input) if v is not None]
	        	idx = idx[len(idx)-1]+1 if len(idx) > 0 else -1
        		if idx >= 0:
            			lastRain = input[idx]
				passedSinceLastRain = (datetime.datetime.now()-input[idx]).total_minutes() 
			if passedSinceLastRain < 360:
                		self.logger.notify('Rained in the last 6 h', 'Not watering because rained')
				resp.should_water = False
                
			return resp
		except Exception as e:
			self.logger.log('ERROR: {0}'.format(e))
			return resp
