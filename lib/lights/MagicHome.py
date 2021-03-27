from lib.lights.Light import Light
import magichue

class MagicHome (Light) :

	def __init__(self, ip, identifier):
		self.mh = magichue.Light(ip)
		super().__init__(ip, identifier)

	def brightness(self, level):
		self.brightnessLevel = level
		self.mh.brightness = level

	def colorRGB(self, red, green, blue):
		self.red = red
		self.green = green
		self.blue = blue 
		self.mh.rgb = (red, green, blue)

	def onOff(self, power):
		self.power = power
		self.mh.on = power
