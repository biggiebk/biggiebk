#!/usr/bin/python3
from lib.audio.PodcastFeed import PodcastFeed
import os

# Get list of podcasts
for show in os.listdir('/home/pi/data/podcasts'): 
	try: 
		podcastFeed = PodcastFeed(show)
		freshDownload = podcastFeed.downloadFeed()
		if freshDownload:
			podcastFeed.saveShowList()
			podcastFeed.cleanDownloads()
			podcastFeed.cleanEpisodes()
	except Exception as e:
		print (e)