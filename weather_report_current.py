import json
import requests
import datetime
from weather_report_base import WeatherReportBase
from private_data import PrivateData
from watering_response import WateringResponse

class WeatherReportCurrent(WeatherReportBase):
	def __init__(self, successor, logger):
        	super(WeatherReportCurrent, self).__init__(successor, logger)
	        self.url = ('http://api.openweathermap.org/data/2.5/weather?id={0}&APPID={1}'.
                     format(PrivateData.CITY_ID, PrivateData.APP_KEY))

	def can_handle(self, input):
        	return True

	def handle_query(self, time):
		resp = WateringResponse()
		print 'wtf'
		self.logger.info("Checking current weather")
        	try:
			now = datetime.datetime.now()
			response = requests.get(self.url)
			w_data = response.json()
			print w_data
			#Check if it is raining
			weather_code = int(w_data[WeatherReportBase.WEATHER_TAG])	
			if weather_code <= WeatherReportBase.RAIN_CODES[1] and \
					weather_code >= WeatherReportBase.RAIN_CODES[0]:
				self.logger.info('Skip watering because of the rain')
				resp.should_water = False
			else:
                		if WeatherReportBase.RAIN_TAG not in w_data:
		                	return resp
				else:
					#check if it rained in the last 3 h
					rain_volume = w_data[WeatherReportBase.RAIN_TAG]['3h'] 
					if  float(rain_volume) > float(PrivateData.RAIN_TRASHOLD):
						resp.should_water = False
						self.logger.info('Skip watering because of the rain')
		except Exception as e:
			self.logger.info('Will water because of error: {0}'.format(str(e)))
		return resp
