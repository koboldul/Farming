import json
import requests
import datetime
from weather_report_base import WeatherReportBase
from private_data import PrivateData
from watering_response import WateringResponse

class WeatherReportForecast(WeatherReportBase):
	def __init__(self, successor, logger):
        	super(WeatherReportForecast, self).__init__(successor, logger)
	        self.url = ('http://api.openweathermap.org/data/2.5/forecast/city?id={0}&APPID={1}'.
                     format(WeatherReportBase.CITY_ID, PrivateData.APP_KEY))

	def should_start_water(self):
		return WateringResponse()

  #      try:
		#	now = datetime.datetime.now()
		#	response = requests.get(url)
		#	w_data = response.json()
		#	for forecast in w_data['list']:
		#		day = datetime.datetime.fromtimestamp(int(forecast['dt'])).strftime('%Y-%m-%d %H')
		
		#		weatherID = int(forecast['weather'][0]['id'])   
		#		if  weatherID < 532 :
		#			print(forecast['weather'])
		#			print 'Will be water!'
		#except Exception as e:
		#	print 'exception : ', str(e)
