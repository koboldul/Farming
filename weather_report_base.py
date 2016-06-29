import json
import requests
import datetime
import abc
from watering_response import WateringResponse

class WeatherReportBase(object):
    __metaclass__ = abc.ABCMeta
    
    RAIN_TAG = 'rain'
    WEATHER_TAG = 'weather'
    RAIN_CODES=[200, 531]

    def __init__(self, successor, logger):
        self.successor = successor
        self.logger = logger

    def get_watering_response(self, input):
        resp = WateringResponse()
        if (self.can_handle):
            resp = self.handle_query(input)
        if resp.should_water and self.successor is not None:
            return self.successor.get_watering_response(input)
        else:
            return resp        

    @abc.abstractmethod
    def handle_query(self, time):
        """Determines if a watering is necessary.Should return a WateringResponse"""
        

    @abc.abstractmethod
    def can_handle(self, input):
        """Code that decides if the class will handle the call"""
        return True
