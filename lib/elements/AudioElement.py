from lib.audio.Player import Player
from lib.audio.PodcastPlayList import PodcastPlayList
import os
import subprocess
import json

class AudioElement():
	def __init__ (self, theme, audioTkDict):
		self.tkDict = audioTkDict
		self.tkDict['playBtn'].setCommand(self.play)
		self.tkDict['pauseBtn'].setCommand(self.pause)
		self.tkDict['stopBtn'].setCommand(self.stop)
		self.tkDict['hBtn'].setCommand(self.high)
		self.tkDict['mBtn'].setCommand(self.med)
		self.tkDict['lBtn'].setCommand(self.low)
		self.tkDict['playPodcastBtn'].setCommand(self.playPodcast)
		self.tkDict['discardPodcastBtn'].setCommand(self.markEpisodePlayed)
#		self.tkDict['restartPodcastBtn']
		self.podPlayList = PodcastPlayList(theme)
		self.theme = theme
		self.tkDict['playingLbl'].setText("Media: Not Playing")
		self.palPlayer = Player()
		self.refreshPlayList()
		self.podcast = False

	# Set the audio element with the dictionary past in
	def setAudio(self, audioJson):
		#read in file
		with open("%saudio/%s.json" %(self.theme.envDir, audioJson), 'r') as imptFile:
			audioJSON=imptFile.read()
		# parse file
		self.audioDict = json.loads(audioJSON)
		# If play is set to true, else stop
		if self.audioDict['play'] == True:
			self.podcast = False
			self.buildOptions()
			self.palPlayer.setPlayer(self.options)
			if self.audioDict['type'] == 'script':
				media = subprocess.check_output(self.audioDict['script'], shell = True)
				self.palPlayer.setMedia(media.decode('ascii').replace("\n",''))
			elif self.audioDict['type'] == 'podcast':
				pass
			self.play()
			self.med()
		else: # Stop
			self.palPlayer.stop()

	def buildOptions(self):
		self.options = ""
		if self.audioDict['loop'] == True:
			self.options = '--input-repeat=999999'
	
	def clean(self):
		self.palPlayer.bye()

	## Player options
	# Player action functions
	def pause(self):
		self.palPlayer.pause()
		self.tkDict['playBtn'].onOff(False)
		self.tkDict['pauseBtn'].onOff(True)
		self.tkDict['stopBtn'].onOff(False)
	def play(self):
		self.palPlayer.play()
		self.tkDict['playingLbl'].setText("Media: %s" %(self.palPlayer.getMedia()).split('.')[0])
		self.tkDict['playBtn'].onOff(True)
		self.tkDict['pauseBtn'].onOff(False)
		self.tkDict['stopBtn'].onOff(False)
	def stop(self):
		self.palPlayer.stop()
		self.tkDict['playBtn'].onOff(False)
		self.tkDict['pauseBtn'].onOff(False)
		self.tkDict['stopBtn'].onOff(True)
	def high(self):
		self.palPlayer.setVolume(self.theme.volHigh)
		self.tkDict['hBtn'].onOff(True)
		self.tkDict['mBtn'].onOff(False)
		self.tkDict['lBtn'].onOff(False)
	def med(self):
		self.palPlayer.setVolume(self.theme.volMed)
		self.tkDict['hBtn'].onOff(False)
		self.tkDict['mBtn'].onOff(True)
		self.tkDict['lBtn'].onOff(False)
	def low(self):
		self.palPlayer.setVolume(self.theme.volLow)
		self.tkDict['hBtn'].onOff(False)
		self.tkDict['mBtn'].onOff(False)
		self.tkDict['lBtn'].onOff(True)

# Podcast actions
	def playPodcast(self):
		if not self.tkDict['playListBox'].isSelected():
			self.tkDict['playListBox'].setItem(0)

		self.currentPodcast = self.podcastPlayDict[self.tkDict['playListBox'].getSelected()]

		with open("%s%s/settings.json" %(self.theme.podcastDir,self.currentPodcast['show']), 'r') as imptFile:
			settingsJSON=imptFile.read()
		# Parse into dictionary
		podcastSettings = json.loads(settingsJSON)
		playMedia = ''
		if os.path.exists("%s%s/downloads/%s.%s" %(self.theme.podcastDir,self.currentPodcast['show'],self.currentPodcast['title'],podcastSettings['fileType'])):
			playMedia = "%s%s/downloads/%s.%s" %(self.theme.podcastDir,self.currentPodcast['show'],self.currentPodcast['title'],podcastSettings['fileType'])
		else:
			playMedia = self.currentPodcast['link']
		self.palPlayer.setPlayer()
		self.palPlayer.setMedia(playMedia)
		self.low()
		self.play()
		self.tkDict['playingLbl'].setText("Media: " + self.currentPodcast['title'])
		self.tkDict['playBtn']
		self.tkDict['pauseBtn']
		self.tkDict['stopBtn']
		self.podcast = True
		self.tkDict['playListBox'].setAfter(5,self.podcastStatus)

	def updatePlayList(self):
		# Find episodes
		podcastPlayList = []
		self.podcastPlayDict = {}
		for episode in self.podPlayList.recent():
			if not episode['played']:
				podcastPlayList.append("%s - %s" %(episode['show'], episode['title']))
				self.podcastPlayDict["%s - %s" %(episode['show'], episode['title'])] = episode
		self.tkDict['playListBox'].setValues(podcastPlayList)

	def refreshPlayList(self):
		self.updatePlayList()
		self.tkDict['playListBox'].setAfter(1800,self.refreshPlayList)

	def markEpisodePlayed(self):
		discardEpisode = self.podcastPlayDict[self.tkDict['playListBox'].getSelected()]
		discardEpisode['played'] = True
		with open("%s%s/episodes/%s.json" %(self.theme.podcastDir,discardEpisode['show'],discardEpisode['title']), 'w') as f:
			json.dump(discardEpisode, f)
		self.updatePlayList()

	def podcastStatus(self):
		if not self.palPlayer.paused and not self.palPlayer.stopped:
			if self.palPlayer.isPlaying() == 0 and self.podcast:
				self.playOldestPodcast()
		if self.podcast:
			self.tkDict['discardPodcastBtn'].setAfter(5,self.podcastStatus)

	def playOldestPodcast(self):
		#Make current played
		self.currentPodcast['played'] = True
		with open("%s%s/episodes/%s.json" %(self.theme.podcastDir,self.currentPodcast['show'],self.currentPodcast['title']), 'w') as f:
			json.dump(self.currentPodcast, f)
		self.updatePlayList()
		self.tkDict['playListBox'].setItem(0)
		self.playPodcast()