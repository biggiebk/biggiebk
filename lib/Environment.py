import sys
import json
import os
import subprocess
from lib.elements.AudioElement import AudioElement
from lib.elements.LightsElement import LightsElement
from lib.elements.WeatherElement import WeatherElement
from datetime import date, time

class Environment () :
	def __init__ (self, theme, envTkDict, audioTkDict, weatherTkDict, calTkDict):
		self.name = 'None'
		self.theme = theme
		self.envTkDict = envTkDict
		self.envTkDict['resetEnvBtn'].setCommand(self.resetEnv)
		self.envTkDict['offEnvBtn'].setCommand(self.offEnv)
		self.envTkDict['setEnvBtn'].setCommand(self.selectEnv)
		self.envTkDict['flipEnvBtn'].setCommand(self.mainFlip)
		self.audioTkDict = audioTkDict
		self.audioEl = AudioElement(theme, audioTkDict)
		self.weatherTkDict = weatherTkDict
		self.weather = WeatherElement( theme, weatherTkDict)
		self.calTkDict = calTkDict
		self.lightsEl = LightsElement(theme)
		self.findEnvOpts()
		self.sober()
	def setEnv(self, name):
		self.name = name
		# read file
		with open("%s%s.json" %(self.theme.envDir, self.name), 'r') as envFile:
			envJSON=envFile.read()
		# parse file
		envDict = json.loads(envJSON)

		if "audio" in envDict:
			self.audioEl.setAudio(envDict['audio'])

		if "importLights" in envDict:
			self.lightsEl.setLights(envDict['importLights'])
		else:
			return

	# Scene action functions
	def selectEnv(self):
		name = self.envTkDict['envListBox'].getSelected()
		self.envTkDict['envLbl'].setText("Scene: *" + name)
		self.envTkDict['envLbl'].update()
		self.setEnv(name)
		self.envTkDict['envLbl'].setText("Scene: " + name)	# Scene action functions
	
	#Flip the main light
	def mainFlip(self):
		self.lightsEl.flip('hue','office1')

	# Scene action functions
	def resetEnv(self):
		self.setEnv('Reset')
		self.envTkDict['envLbl'].setText("Env: None")
	def offEnv(self):
		self.setEnv('LightsOff')
		self.envTkDict['envLbl'].setText("Env: None")
	def findEnvOpts(self):
		# Find Env Options
		envs = []
		for entry in os.listdir(self.theme.envDir): 
			if entry.endswith('.json'): 
				if entry != 'Reset.json' and entry != 'LightsOff.json' and entry != 'Podcast.json':
					envs.append(entry.replace('.json',''))
		# Sort
		envs.sort()
		self.envTkDict['envListBox'].setValues(envs)
	# Sober Since
	def sober(self):
		soberDay = date(2020,6,25)
		days = (date.today()-soberDay).days
		self.calTkDict['soberLbl'].setText("Days Sober: %i" %(days))
		self.calTkDict['soberLbl'].setAfter(600, self.sober)
	def clean(self):
		self.audioEl.clean()