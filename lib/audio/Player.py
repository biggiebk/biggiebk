import vlc

class Player () :
	def __init__ (self, options=''):
		self.player = vlc.Instance(options)
		self.paused = False
		self.stopped = False

	def bye(self):
		try:
			self.stop()
			self.media_list_player.get_media_player().release()
			del self.media
			del self.media_list_player
			self.player.release
			del self.player
		except AttributeError:
			pass # do nothing we know this may blow up if something has not already started to play

	def getLength(self):
		return self.media_list_player.get_media_player().get_length()

	def getMedia(self):
		return self.media.get_meta(0)

	def getPlace(self):
		return self.media_list_player.get_media_player().get_time()

	def isPlaying(self):
		return self.media_list_player.get_media_player().is_playing()

	def pause(self):
		self.paused = True
		self.stopped = False
		self.media_list_player.pause()

	def play(self):
		self.paused = False
		self.stopped = False
		self.media_list_player.play() 

	def setMedia(self, mediaFile):
		# creating a new media list 
		self.media_list = self.player.media_list_new() 
  	# creating a media player object 
		self.media_list_player = self.player.media_list_player_new()
		# creating a new media 
		self.media = self.player.media_new(mediaFile)
		# adding media to media list 
		self.media_list.add_media(self.media)
		# setting media list to the mediaplayer 
		self.media_list_player.set_media_list(self.media_list)
		self.play()

	def setPlace(self, place):
		self.media_list_player.get_media_player().set_time(int(place))

	def setPlayer(self, options=''):
		self.bye()
		self.player = vlc.Instance(options)

	def setVolume(self, vol):
		self.media_list_player.get_media_player().audio_set_volume(int(vol))

	def stop(self):
		self.stopped = True
		self.media_list_player.get_media_player().stop()