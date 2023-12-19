# app.py
from flask import Flask, render_template, request
import numpy as np
from netCDF4 import Dataset
from PIL import Image
from geopy.geocoders import Nominatim

app = Flask(__name__)

# Load weather data
file = 'RF25_ind2022_rfp25.nc'
data = Dataset(file, mode='r')

# Extract latitude, longitude, time, and rainfall data
lats = data.variables['LATITUDE'][:]
longs = data.variables['LONGITUDE'][:]
time = data.variables['TIME'][:]
tave = data.variables['RAINFALL'][:]

# Use geopy to obtain coordinates for Indian cities
geolocator = Nominatim(user_agent="city_coordinates")
indian_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]

city_coordinates = {}
for city in indian_cities:
    location = geolocator.geocode(city + ", India")
    if location:
        city_coordinates[city] = (location.latitude, location.longitude)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_day = int(request.form['day'])
        selected_city = request.form['city']
    else:
        selected_day = 1  # Default to the first day
        selected_city = "Mumbai"  # Default city

    # Calculate average rainfall for the selected day and city
    lat, lon = city_coordinates[selected_city]
    location_lat_range = np.where((lats >= lat - 0.25) & (lats <= lat + 0.25))[0]
    location_lon_range = np.where((longs >= lon - 0.25) & (longs <= lon + 0.25))[0]
    rainfall_values = tave[selected_day - 1, location_lat_range, :][:, location_lon_range]
    avg_rainfall = np.mean(rainfall_values)

    return render_template('index.html', lats=lats, longs=longs, time=time, city_coordinates=city_coordinates,
                           selected_day=selected_day, selected_city=selected_city, avg_rainfall=avg_rainfall)

if __name__ == '__main__':
    app.run(debug=True)
