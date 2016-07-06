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
        	try:
			response = requests.get(self.url)
			w_data = response.json()
			#Check if it is raining
			weather_code = int(w_data[WeatherReportBase.WEATHER_TAG][0]['id'])	
               		itRained = False
			if WeatherReportBase.RAIN_TAG  in w_data and  '3h' in w_data[WeatherReportBase.RAIN_TAG]:
				rain_volume = float(w_data[WeatherReportBase.RAIN_TAG]['3h']) 
				if rain_volume > PrivateData.RAIN_TRASHOLD:
					itRained = True	
			else:
				if weather_code<= WeatherReportBase.RAIN_CODES[1] and \
		        		weather_code >= WeatherReportBase.RAIN_CODES[0] and \
					weather_code not in WeatherReportBase.NOT_ENOUGH_RAIN :
					itRained = True
			if itRained:
				self.logger.log(str(w_data))
				resp.rainedAt = datetime.datetime.now()
				resp.should_water = False
				self.logger.log('Raining right now. {0}'.format(datetime.datetime.now()))
		except Exception as e:
			self.logger.log('Error getting the current weather: {0}'.format(str(e)))

		return resp
