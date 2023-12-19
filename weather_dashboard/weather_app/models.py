# weather_app/models.py
from django.db import models

class WeatherData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_time = models.DateTimeField()
    rainfall = models.FloatField()
