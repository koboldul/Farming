import json
import requests
import datetime

url = 'http://api.openweathermap.org/data/2.5/forecast/city?id={0}&APPID={1}'. \
		format(6176823, '11be13faae799ffc574b476e76ba3f99')
print datetime.datetime.now()

try:
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

