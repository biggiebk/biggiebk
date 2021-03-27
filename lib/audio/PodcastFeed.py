#!/usr/bin/python3
import feedparser
import json
import requests
import datetime
import glob 
import os 

class PodcastFeed () :
	def __init__ (self,name):
		self.name = name
		self.directory = "/home/pi/data/podcasts/%s/" %(self.name)
		with open("%ssettings.json" %(self.directory), 'r') as imptFile:
			settingsJSON=imptFile.read()
		# Parse into dictionary
		self.settings = json.loads(settingsJSON)
		with open("%sstatus.json" %(self.directory), 'r') as lastFile:
			lastStatus=lastFile.read()
		self.lastStatus = json.loads(lastStatus)
		self.episodes = []
		self.downloads = []

	# clean downloads
	def cleanDownloads(self):
		for file in glob.glob("%sdownloads/*.%s" %(self.directory,self.settings['fileType'])):
			if not file in self.downloads:
				os.remove(file)

	# clean episodes
	def cleanEpisodes(self):
		for file in glob.glob("%sepisodes/*.json" %(self.directory)):
			if not file in self.episodes:
				os.remove(file)
	
	# Get Show List
	def downloadFeed(self):
		session = requests.Session()
		session.headers.update({'User-Agent': 'bryce@mymadlab.net Vallejo, CA GO USA!', 'If-None-Match': self.lastStatus['ETag']})
		response = session.get(self.settings['url'], stream = True)
		if response.status_code != 304:
			self.currentStatus = {}
			if 'ETag' in response.headers:
				self.currentStatus['ETag'] = response.headers['ETag'].replace('"', '')
			else:
				self.currentStatus['ETag'] = "0"
			with open("%sfeed.rss" %(self.directory),'wb') as feedFile: 
				for chunk in response.iter_content(chunk_size=1024):
					if chunk: 
						feedFile.write(chunk)
			# Save Status
			self.saveStatus()
			return True
		else:
			return False
			
	# Download Show
	def downloadShow(self, name, url):
		session = requests.Session()
		session.headers.update({'User-Agent': 'bryce@mymadlab.net Vallejo, CA GO USA!', 'If-None-Match': self.lastStatus['ETag']})
		response = session.get(url, stream = True)
		with open("%sdownloads/%s" %(self.directory,name),'wb') as showFile: 
			for chunk in response.iter_content(chunk_size=1024):
				if chunk: 
					showFile.write(chunk)

	def saveShowList(self):
		rssFeed = feedparser.parse("%sfeed.rss" %(self.directory))
		for entry in range(self.settings['maxTrackNumber']):
			episodeDict = {}
			episodeDict['title'] = rssFeed.entries[entry].title.replace('/','-').replace(':', '')
			episodeDict['description'] = rssFeed.entries[entry].description
			for link in rssFeed.entries[entry].links:
				if link.rel == 'enclosure':
					episodeDict['link'] = link.href
			episodeDict['played'] = False
			episodeDict['keep'] = False
			episodeDict['location'] = 0
			episodeDict['show'] = self.name
			published = datetime.datetime.strptime(rssFeed.entries[entry].published,'%a, %d %b %Y %H:%M:%S %z')
			episodeDict['published'] = "%s" %(published.strftime('%m/%d/%Y'))
			if not os.path.exists("%sepisodes/%s.json" %(self.directory,episodeDict['title'])):
				with open("%sepisodes/%s.json" %(self.directory,episodeDict['title']), 'w') as f:
					json.dump(episodeDict, f)
			self.episodes.append("%sepisodes/%s.json" %(self.directory,episodeDict['title']))
			if entry < self.settings['historicalDownloads']:
				name = "%s.%s" %(episodeDict['title'],self.settings['fileType'])
				self.downloads.append("%sdownloads/%s" %(self.directory,name))
				if not os.path.exists("%sdownloads/%s" %(self.directory,name)):
					self.downloadShow(name,episodeDict['link'])

	def saveStatus(self):
		with open("%sstatus.json" %(self.directory), 'w') as f:
			json.dump(self.currentStatus, f)
