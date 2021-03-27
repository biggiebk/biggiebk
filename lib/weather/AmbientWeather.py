import json
import requests

class AmbientWeather:
	def __init__ (self):
		self.appKey = '90124b38ea52438d947cf98f110b8266c2e03fcdd2044c84a149e4e89f084cd0'
		self.apiKey = '7967b9ca273d4b8f99db53c0da2b6d31704462d1ca504f68a69d19b1567b5528'
	
	def getDevices(self):
		self.session = requests.Session()
		results = self.session.get("https://api.ambientweather.net/v1/devices?applicationKey=%s&apiKey=%s" %(self.appKey,self.apiKey))
#		print(results.content)
		return results.content
