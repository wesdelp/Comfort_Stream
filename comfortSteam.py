#!/usr/bin/python

# Wes Delp
# Internet of Things
# Comfort Data Stream
# 07.26.2014

import time
import sys
import Adafruit_DHT
# May integrate light...
import analog as lightsensor
import requests
import math

# DHT22 Temperature and Humidity Sensor Setup
sensor = 22
pin = 4

# Photoresistor Pin Setup
channel = 0
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# Stream Static Data
name = "Location Name"
lat = 39.99
lon = -82.81
zip = 43004

# Humidex Comfort Zones
comfort = {}
comfort[29]="No Discomfort"
comfort[39]="Some Discomfort"
comfort[45]="Great Discomfort"
comfort[54]="Dangerous"
comfort[55]="Extremely Dangerous"

# Convert C to F
def celToFar(temp):
	return (temp * 1.8 + 32)

# Calculate the humidex (feels like) temperature
def getHumidex(temp,humidity):
	dewpoint = temp - ((100-humidity)/5.0)
	humidex = round(temp + (3.39556) * 
	math.exp(19.8336 - 5417.75/(dewpoint+273.15)) - 5.5556, 2)
	return humidex

# Get comfort zone
def getComfortZone(humidex):
	for item in sorted(comfort):
		if (humidex <= item):
			return comfort[item]
		if (humidex > 55):
			return comfort[55]

# Post data to stream and return status
def post_data(comfortZone, humidex, humidity, lat, light, lon, name, temp, zip):
	req = requests.get("http://data.sparkfun.com/input/robqvbvK2DIzzzoZX9Q4?" +
	"private_key=" +
	"&comfortzone=" + comfortZone +
	"&humidex=" + str(humidex) +
	"&humidity=" + str(humidity) +
	"&lat=" + str(lat) +
	"&light=" + str(light) +
	"&lon=" + str(lon) +
	"&name=" + name +
	"&temp=" + str(temp) +
	"&zip=" + str(zip))
	return req.status_code

statusCode = 200	
while(statusCode == 200):
	light = lightsensor.readadc(channel, SPICLK, SPIMOSI, SPIMISO, SPICS)
	humidity, temp = Adafruit_DHT.read_retry(sensor, pin)
	temp = round(celToFar(temp),2)
	humidity = round(humidity,2)
	humidex = getHumidex(temp, humidity)
	comfortZone = getComfortZone(humidex)
	
	print light
	print temp,"F"
	print humidity,"%"
	print humidex
	print comfortZone
	print "Post Successful!\n"
	
	statusCode = post_data(comfortZone, humidex, humidity, lat, light, lon, name, temp, zip)
	
	time.sleep(60.0)

