import json
import requests
import datetime

class WeatherReport:i
	CITY_ID = 6176823 #Waterloo CA
	APP_KEY = ''
	
	def __init__(self, logger):
		self.url = 'http://api.openweathermap.org/data/2.5/forecast/city?id={0}&APPID={1}'.
			format(CITY_ID, APP_KEY)
	def should_start_water(self):
		try:
			now = datetime.datetime.now()
			response = requests.get(url)
			w_data = response.json()
			for forecast in w_data['list']:
				day = datetime.datetime.fromtimestamp(int(forecast['dt'])).strftime('%Y-%m-%d %H')
		
				weatherID = int(forecast['weather'][0]['id'])   
				if  weatherID < 532 :
					print(forecast['weather'])
					print 'Will be water!'
		except Exception as e:
			print 'exception : ', str(e)
