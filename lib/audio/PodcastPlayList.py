import json
import datetime
import glob 
import os 

class PodcastPlayList () :
	def __init__ (self,theme):
		self.theme = theme
		self.episodes = []
		self.loadList()
		
	def loadList(self):
		self.episodes = []
		for show in os.listdir(self.theme.podcastDir):
			with open("%s%s/settings.json" %(self.theme.podcastDir, show), 'r') as settingsFile:
				settingsJSON=settingsFile.read()
			# parse file
			settingsDict = json.loads(settingsJSON)
			for episode in os.listdir("%s%s/downloads" %(self.theme.podcastDir, show)):
				with open("%s%s/episodes/%s.json" %(self.theme.podcastDir, show,episode.replace(".%s" %(settingsDict['fileType']),'')), 'r') as episodeFile:
					episodeJSON=episodeFile.read()
				# parse file
				episodeDict = json.loads(episodeJSON)
				self.episodes.append(episodeDict)

	def recent(self):
		return sorted(self.episodes, key = lambda i: i['published'])