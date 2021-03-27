from tkinter import Button
from lib.gui.Theme import Theme

class PalButton():
	def __init__(self, frame, text, theme, **kwargs):
		self.frame = frame
		self.text = text
		self.theme = theme
		self.button = Button(self.frame, text = self.text, foreground = self.theme.light, background = self.theme.dark, highlightbackground=self.theme.dark, **kwargs)

	def onOff(self, on):
		if on:
			self.button.configure(foreground = self.theme.dark, background = self.theme.light)
		else:
			self.button.configure(foreground = self.theme.light, background = self.theme.dark)

	def setAfter(self, seconds, cmd):
		self.button.after(seconds * 1000, cmd)

	def setCommand(self, cmd):
		self.button.configure(command = cmd)
		self.update()

	def setGrid(self, **kwargs):
		self.button.grid(kwargs)

	def setText(self, textUpdate):
		self.text = textUpdate
		self.button.configure(text = self.text)

	def update(self):
		self.button.update()
