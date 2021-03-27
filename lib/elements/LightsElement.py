from lib.lights.MagicHome import MagicHome 
from lib.lights.Tuya import Tuya
from lib.lights.PhilipsHue import PhilipsHue
import json

class LightsElement():
	def __init__ (self, theme):
		self.theme = theme

	def setLight(self, light):
		#read in file
		with open("%slights/%s.json" %(self.theme.envDir, light), 'r') as imptFile:
			lightJSON=imptFile.read()
		# parse file
		lightDict = json.loads(lightJSON)
		device = None
		if lightDict['vendor'] == 'magicHome':
			with open("%smagicHueStatus.json" %(self.theme.deviceDir), 'r') as statusFile:
				statusJSON = statusFile.read()
			# parse file
			statusDict = json.loads(statusJSON)
			for status in statusDict:
				if status['name'] == lightDict['name']:
					device = MagicHome(status['ip'], status['identifier'])
		elif lightDict['vendor'] == 'tuya':
			with open("%stuyaStatus.json" %(self.theme.deviceDir), 'r') as statusFile:
				statusJSON = statusFile.read()
			# parse file
			statusDict = json.loads(statusJSON)
			for status in statusDict:
				if status['name'] == lightDict['name']:
					device = Tuya(status['key'], status['ip'], status['identifier'])
		elif lightDict['vendor'] == 'hue':
			with open("%sphilipsHue.json" %(self.theme.deviceDir), 'r') as statusFile:
				statusJSON = statusFile.read()
			# parse file
			statusDict = json.loads(statusJSON)
			for status in statusDict:
				if status['name'] == lightDict['name']:
					device =  PhilipsHue(status['instance'], status['identifier'])
		try:
			device.setStatus(lightDict['power'], lightDict['red'], lightDict['green'], lightDict['blue'], lightDict['brightness'])
		except Exception as e:
			print(e)

	def setLights(self, Lights):
		for light in Lights:
			self.setLight(light)

	def flip(self, vendor, name):
		device = None
		if vendor == 'magicHome':
			with open("%smagicHueStatus.json" %(self.theme.deviceDir), 'r') as statusFile:
				statusJSON = statusFile.read()
			# parse file
			statusDict = json.loads(statusJSON)
			for status in statusDict:
				if status['name'] == name:
					device = MagicHome(status['ip'], status['identifier'])
		elif vendor == 'tuya':
			with open("%stuyaStatus.json" %(self.theme.deviceDir), 'r') as statusFile:
				statusJSON = statusFile.read()
			# parse file
			statusDict = json.loads(statusJSON)
			for status in statusDict:
				if status['name'] == name:
					device = Tuya(status['key'], status['ip'], status['identifier'])
		elif vendor == 'hue':
			with open("%sphilipsHue.json" %(self.theme.deviceDir), 'r') as statusFile:
				statusJSON = statusFile.read()
			# parse file
			statusDict = json.loads(statusJSON)
			for status in statusDict:
				if status['name'] == name:
					device =  PhilipsHue(status['instance'], status['identifier'])
			device.flip()