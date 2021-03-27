from tkinter import Label
from lib.gui.Theme import Theme

class PalLabel():
	def __init__(self, frame, text, theme, **kwargs):
		self.frame = frame
		self.text = text
		self.theme = theme
		self.label = Label(self.frame, text = self.text, foreground = self.theme.light, background = self.theme.dark, **kwargs)

	def onOff(self, on):
		if on:
			self.label.configure(background = self.theme.light, foreground = self.theme.dark)
		else:
			self.label.configure(background = self.theme.dark, foreground = self.theme.light)

	def setAfter(self, seconds, cmd):
		self.label.after(seconds * 1000, cmd)

	def setCommand(self, cmd):
		self.label.configure(command = cmd)

	def setGrid(self, **kwargs):
		self.label.grid(kwargs)

	def setText(self, textUpdate):
		self.text = textUpdate
		self.label.configure(text = self.text)
		self.update()
	
	def update(self):
		self.label.update()