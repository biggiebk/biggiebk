import json
import requests

class NationalWeatherService:
	def __init__ (self):
		self.lon = '-122.1998204'
		self.lat = '38.07009180000001'
		self.userAgent = 'bryce@mymadlab.net Vallejo, CA GO USA!'
		self.office = 'STO'
		self.gridX = '11'
		self.gridY = '50'
	
	def getForcast(self):
		self.session = requests.Session()
		self.session.headers.update({'User-Agent': self.userAgent})
		#results = self.session.get("https://api.weather.gov/gridpoints/%s/%s,%s/forecast" %(self.office,self.gridX,self.gridY))
		results = self.session.get("https://api.weather.gov/gridpoints/%s/%s,%s" %(self.office,self.gridX,self.gridY))
		return results.content
	
	def getGrid(self):
		self.session = requests.Session()
		self.session.headers.update({'User-Agent': self.userAgent})
		results = self.session.get("https://api.weather.gov/points/%s,%s" %(self.lat,self.lon))
		return results.content

