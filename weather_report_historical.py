import json
import requests
import datetime
from weather_report_base import WeatherReportBase
from private_data import PrivateData
from watering_response import WateringResponse

class WeatherReportHistorical(WeatherReportBase):
	def __init__(self, successor, logger):
        	super(WeatherReportCurrent, self).__init__(successor, logger)

	def can_handle(self, input):
        	return len(input) > 0

	def handle_query(self, input):
		resp = WateringResponse()
		
		return resp
