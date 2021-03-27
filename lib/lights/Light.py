import time

class Light():
	def __init__(self, ip, identifier):
		self.ip = ip
		self.identifier = identifier

	def brightness(self, level):
		pass

	def colorRGB(self, red, green, blue):
		pass

	def flip(self):
		pass

	def onOff(self, power):
		pass

	def setStatus(self, power, red, green, blue, brightnessLevel, blink = 0, fade = 0):
		self.power = power
		self.red = red
		self.green = green
		self.blue = blue
		self.brightnessLevel = brightnessLevel
		self.blink = blink
		self.fade = fade
		self.update()

	def update(self):
		if self.power:
			self.colorRGB(self.red, self.green, self.blue)
			self.brightness(self.brightnessLevel)
		self.onOff(self.power)