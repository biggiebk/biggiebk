from lib.weather.AmbientWeather import AmbientWeather
from lib.weather.NationalWeatherService import NationalWeatherService
from datetime import date, datetime, timedelta
import json

class WeatherElement():
	def __init__ (self, theme, weatherTkDict):
		self.tkDict = weatherTkDict
		self.theme = theme
		self.ambw = AmbientWeather()
		self.nsw = NationalWeatherService()
		self.weather()

	def weather(self):
		try:
			content = json.loads(self.ambw.getDevices())
			homeOutdoor = content[0]['lastData']['tempf'] # Outdoor
			homeIndoor = content[0]['lastData']['tempinf'] # Indoor
		except Exception as e:
			print (e)
		try:
			nswContent = json.loads(self.nsw.getForcast())
			high = (nswContent['properties']['maxTemperature']['values'][0]['value'] * 1.800) + 32 # High
			low = (nswContent['properties']['minTemperature']['values'][0]['value'] * 1.800) + 32 # Low
			tomHigh = (nswContent['properties']['maxTemperature']['values'][1]['value'] * 1.800) + 32 # High
			tomLow = (nswContent['properties']['minTemperature']['values'][1]['value'] * 1.800) + 32 # Low
			chanceOfRain = 0
			tomChanceOfRain = 0
			for value in nswContent['properties']['probabilityOfPrecipitation']['values']:
				iso = value['validTime'].split('/')[0]
				date1 = datetime.fromisoformat(iso)
				if date1.date() == date.today():
					if value['value'] > chanceOfRain:
						chanceOfRain = value['value']
				if date1.date() == date.today() + timedelta(1):
					if value['value'] > tomChanceOfRain:
						tomChanceOfRain = value['value']
				# If two days from now exit
				if date1.date() > date.today() + timedelta(1):
						break
			if chanceOfRain >= 60:
				self.tkDict['wthrLbl'].setText("Temp: %s/%s\n H/L: %i/%i\nCoR: %i" %(homeOutdoor,homeIndoor,high,low,chanceOfRain)) 
			elif chanceOfRain >= 40:
				self.tkDict['wthrLbl'].setText("Temp: %s/%s\n H/L: %i/%i\nCoR: %i" %(homeOutdoor,homeIndoor,high,low,chanceOfRain)) 
			else:
				self.tkDict['wthrLbl'].setText("Temp: %s/%s\n H/L: %i/%i\nCoR: %i" %(homeOutdoor,homeIndoor,high,low,chanceOfRain))

			if tomChanceOfRain >= 60:
				self.tkDict['tomWthrLbl'].setText("Tomorrow\n H/L: %i/%i\nCoR: %i" %(tomHigh,tomLow,tomChanceOfRain)) 
			elif tomChanceOfRain >= 40:
				self.tkDict['tomWthrLbl'].setText("Tomorrow\n H/L: %i/%i\nCoR: %i" %(tomHigh,tomLow,tomChanceOfRain)) 
			else:
				self.tkDict['tomWthrLbl'].setText("Tomorrow\n H/L: %i/%i\nCoR: %i" %(tomHigh,tomLow,tomChanceOfRain))
		except Exception as e:
			print (e)
		self.tkDict['wthrLbl'].setAfter(90, self.weather)