#!/usr/bin/python3
from tkinter import Tk, Frame, W, E, N, S
from lib.gui.Theme import Theme
from lib.gui.PalButton import PalButton
from lib.gui.PalLabel import PalLabel
from lib.gui.PalListbox import PalListbox
from lib.Environment import Environment
import os
import time
import json

#Set Theme
theme = Theme('#000C18', '#4C7CB0', '#C9DBEE', 100, 75, 60, '/home/pi/data/environments/', '/home/pi/data/devices/','/home/pi/Music/', '/home/pi/data/podcasts/')

root=Tk()
# root window title and colors
root.title("Personal Automation Liberator")
root.configure(background = theme.dark, highlightbackground=theme.middle)
 
#Top Frame
topFrame = Frame(root, background = theme.dark)

## Environment
envTkDict = {}
envFrame = Frame(topFrame) 
envTkDict['envListBox'] = PalListbox(envFrame, theme, height = 7) 
envTkDict['envListBox'].setYscroll()
envBtnsFrame = Frame(topFrame)
envTkDict['resetEnvBtn'] = PalButton(envBtnsFrame, 'R', theme)
envTkDict['offEnvBtn'] = PalButton(envBtnsFrame, 'O', theme)
envTkDict['flipEnvBtn'] = PalButton(envBtnsFrame, 'Flip', theme)
envTkDict['setEnvBtn'] = PalButton(envBtnsFrame, 'Set', theme)
envTkDict['envLbl'] = PalLabel(topFrame, "Env: None", theme)

## Audio
# Audio Frames
audioTkDict = {}
playerFrame = Frame(topFrame) 
volumeFrame = Frame(playerFrame)
playListFrame = Frame(root, background = theme.dark)
podCtrlsFrame = Frame(playListFrame, background = theme.dark)
# Media Label
audioTkDict['playingLbl'] = PalLabel(playListFrame, 'Media: Not Playing', theme)
# Audio Control Buttons
audioTkDict['playBtn'] = PalButton(playerFrame, 'Play', theme)
audioTkDict['pauseBtn'] = PalButton(playerFrame, 'Pause', theme)
audioTkDict['stopBtn'] = PalButton(playerFrame, 'Stop', theme)
#Volume
audioTkDict['hBtn'] = PalButton(volumeFrame, 'H', theme)
audioTkDict['mBtn'] = PalButton(volumeFrame, 'M', theme)
audioTkDict['lBtn'] = PalButton(volumeFrame, 'L', theme)
#Podcast Controls
audioTkDict['playListBox'] = PalListbox(playListFrame, theme, height = 7, width = 97)
audioTkDict['playListBox'].setYscroll()
audioTkDict['playPodcastBtn'] = PalButton(podCtrlsFrame, '^', theme)
audioTkDict['restartPodcastBtn'] = PalButton(podCtrlsFrame, '<', theme)
audioTkDict['discardPodcastBtn'] = PalButton(podCtrlsFrame, 'X', theme)

#Notifications
noteFrame = Frame(topFrame, background = theme.dark, padx=2)

# Calendar
calTkDict = {}
calTkDict['soberLbl'] = PalLabel(noteFrame, 'sober', theme)
# Weather
weatherTkDict ={}
weatherTkDict['wthrLbl'] = PalLabel(noteFrame, 'today', theme, borderwidth=2, relief="raised")
# Tomorrow Weather
weatherTkDict['tomWthrLbl'] = PalLabel(noteFrame, 'tomorrow', theme)

#Iinitiate Environment
env = Environment(theme, envTkDict, audioTkDict, weatherTkDict, calTkDict)

## Setup Grid
topFrame.grid(column=0, row=0, columnspan=2, sticky=W)
# Top Notification Area
envTkDict['envLbl'].setGrid(column=0, row=0, columnspan=2, sticky=W)
# Environment Boxes
envFrame.grid(column=0, row=1, columnspan=2)
envTkDict['envListBox'].setGrid(column=1, row=0)
envTkDict['envListBox'].yScrollBar.grid(column=0, row=0, sticky=N+S)
# Button Area
envBtnsFrame.grid(column=2, row=1, sticky=N+S)
envTkDict['resetEnvBtn'].setGrid(column=0, row=0, ipady=5, sticky=E+W)
envTkDict['offEnvBtn'].setGrid(column=1, row=0, ipady=5, sticky=E+W)
envTkDict['flipEnvBtn'].setGrid(column=0, row=1, columnspan=2, ipady=5, sticky=E+W)
envTkDict['setEnvBtn'].setGrid(column=0, row=2, columnspan=2, ipady=9, sticky=E+W)
playerFrame.grid(column=3, row=1)
audioTkDict['playBtn'].setGrid(column=0, row=0, sticky=W+E)
audioTkDict['pauseBtn'].setGrid(column=0, row=1, sticky=W+E)
audioTkDict['stopBtn'].setGrid(column=0, row=2, sticky=W+E)
volumeFrame.grid(column=0, row=3)
audioTkDict['lBtn'].setGrid(column=0, row=0, ipady=3, sticky=W+E)
audioTkDict['mBtn'].setGrid(column=1, row=0, ipady=3, sticky=W+E)
audioTkDict['hBtn'].setGrid(column=2, row=0, ipady=3, sticky=W+E)
# Notication Panel
noteFrame.grid(column=6, row=0, rowspan = 5, sticky=N)
calTkDict['soberLbl'].setGrid(column=0, row=0, sticky=N+W+E)
weatherTkDict['wthrLbl'].setGrid(column=0, row=1, sticky=N+W+E)
weatherTkDict['tomWthrLbl'].setGrid(column=0, row=2, sticky=N+W+E)
#Play List
playListFrame.grid(column=0, row=1, columnspan=2, sticky=W+E)
audioTkDict['playingLbl'].setGrid(column=0, row=0, columnspan=2, sticky=W)
audioTkDict['playListBox'].yScrollBar.grid(column=0, row=1, sticky=N+S)
audioTkDict['playListBox'].setGrid(column=1, row=1, sticky=W)
podCtrlsFrame.grid(column=0, row=2, columnspan=2)
audioTkDict['playPodcastBtn'].setGrid(column=0, row=0)
#audioTkDict['restartPodcastBtn'].setGrid(column=1, row=0)
audioTkDict['discardPodcastBtn'].setGrid(column=1, row=0)

# Execute Tkinter
root.mainloop()
env.clean()