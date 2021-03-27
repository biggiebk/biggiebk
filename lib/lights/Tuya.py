from lib.lights.Light import Light
import tinytuya

class Tuya (Light) :

	def __init__(self, key, ip, identifier):
		self.tuya = tinytuya.BulbDevice(identifier, ip, key)
		self.tuya.set_version(3.3)
		super().__init__(ip, identifier)

	def brightness(self, level):
		self.brightnessLevel = level
		self.tuya.set_brightness(level)

	def colorRGB(self, red, green, blue):
		self.red = red
		self.green = green
		self.blue = blue 
		self.tuya.set_colour(red, green, blue)

	def onOff(self, power):
		self.power = power
		if power:
			self.tuya.turn_on()
		else:
			self.tuya.set_colour(0, 0, 255)
			self.tuya.turn_off()

	def update(self):
		self.onOff(self.power)
		if self.power:
			self.brightness(self.brightnessLevel)
			self.colorRGB(self.red, self.green, self.blue)
