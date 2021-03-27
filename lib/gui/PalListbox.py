from tkinter import Listbox, Scrollbar, END
from lib.gui.Theme import Theme

class PalListbox():
	def __init__(self, frame, theme, **kwargs):
		self.frame = frame
		self.theme = theme
		self.listbox = Listbox(self.frame, foreground = self.theme.dark, background = self.theme.middle, highlightbackground=self.theme.dark, **kwargs)

	def getSelected(self):
		return self.listbox.get(self.listbox.curselection())

	def isSelected(self):
		if self.listbox.curselection():
			return True
		else:
			return False

	def setAfter(self, seconds, cmd):
		self.listbox.after(seconds * 1000, cmd)

	def setCommand(self, cmd):
		self.listbox.configure(command = cmd)

	def setGrid(self, **kwargs):
		self.listbox.grid(kwargs)

	def setHeight(self, hght):
		self.listbox.configure(height = hght)

	def setItem(self,item):
		self.listbox.select_set(item)

	def setValues(self, values):
		self.listbox.delete(0,END)
		for value in values:
			self.listbox.insert(END, value)

	def setWidth(self, wdth):
		self.listbox.configure(width = wdth)
	
	def setYscroll(self):
		self.yScrollBar = Scrollbar(self.frame)
		self.listbox.config(yscrollcommand = self.yScrollBar.set)
		self.yScrollBar.config(command = self.listbox.yview, troughcolor = self.theme.middle, highlightbackground=self.theme.dark, bg = self.theme.dark, width=22, bd = 0)