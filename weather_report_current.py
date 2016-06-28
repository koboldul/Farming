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
		self.logger.info("Checking current weather")
        	try:
			response = requests.get(self.url)
			w_data = response.json()
			#Check if it is raining
               		if WeatherReportBase.RAIN_TAG not in w_data:
				return resp	
			rain_volume = w_data[WeatherReportBase.RAIN_TAG]['3h'] 
			weather_code = int(w_data[WeatherReportBase.WEATHER_TAG])	
			if weather_code <= WeatherReportBase.RAIN_CODES[1] and \
					weather_code >= WeatherReportBase.RAIN_CODES[0] and \
					float(rain_volume) > float(PrivateData.RAIN_TRASHOLD):
				resp.should_water = False
				self.logger.info('Skip watering because of the rain. Raining right now.')
				resp.should_water = False
		except Exception as e:
			self.logger.info('Will water because of error: {0}'.format(str(e)))
		return resp
