from lib.lights.Light import Light
from hue_api import HueApi

class PhilipsHue (Light) :

	def __init__(self, ip, identifier):
		self.hueApi = HueApi()
		self.hueApi.load_existing()
		self.hueApi.fetch_lights()
		super().__init__(ip, identifier)

	def brightness(self, level):
		self.brightnessLevel = level
		self.hueApi.set_brightness(level)

	def flip(self):
		self.hueApi.toggle_on()

	def onOff(self, power):
		if power:
			self.hueApi.turn_on(self.ip)
		else:
			self.hueApi.turn_off(self.ip)



