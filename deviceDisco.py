#!/usr/bin/python3

import json
from magichue import discover_bulbs
import tinytuya
from hue_api import HueApi

# read lights.json file
with open('/home/pi/data/devices/lights.json', 'r') as lightsFile:
	lightsData=lightsFile.read()
# parse lights file
lights = json.loads(lightsData)

# read old
with open('/home/pi/data/devices/magicHueStatus.json', 'r') as lightsFile:
	lightsData=lightsFile.read()
# parse lights file
oldmhs = json.loads(lightsData)

with open('/home/pi/data/devices/tuyaStatus.json', 'r') as lightsFile:
	lightsData=lightsFile.read()
# parse lights file
oldts = json.loads(lightsData)

with open('/home/pi/data/devices/philipsHue.json', 'r') as lightsFile:
	lightsData=lightsFile.read()
# parse lights file
oldhps = json.loads(lightsData)

# Setup arrays for devices
magicHueDevices = []
tuyaDevices = []
philipsHueDevices = []
for light in lights:
	if light['vendor'] == 'magicHome':
		light['ip'] = oldts[0]['ip']
		magicHueDevices.append(light)
	elif light['vendor'] == 'tuya':
		light['ip'] = oldmhs[0]['ip']
		tuyaDevices.append(light)
	elif light['vendor'] == 'hue':
		light['instance'] = oldhps[0]['instance']
		philipsHueDevices.append(light)

# Discover magicHue devices
for bulb in discover_bulbs():
	for mhd in magicHueDevices:
		fields = bulb.split(",")
		if fields[1] == mhd['identifier']:
			mhd['ip'] = fields[0]

with open('/home/pi/data/devices/magicHueStatus.json', 'w') as f:
	json.dump(magicHueDevices, f)

# Discover tinytuya devices
tempTuya = tinytuya.deviceScan(False,50)
for tt in tempTuya:
	for td in tuyaDevices:
		if tempTuya[tt]['gwId'] == td['identifier']:
			td['ip'] = tt

#Save discovered devices to ~/data/devices/lightsStatus.json
with open('/home/pi/data/devices/tuyaStatus.json', 'w') as f:
	json.dump(tuyaDevices, f)

# Discover philips hue devices
hueApi = HueApi()
hueApi.load_existing()
tempHues = hueApi.fetch_lights()
for hue in range(len(tempHues)):
	for phd in philipsHueDevices:
		if tempHues[hue].name == phd['identifier']:
			phd['instance'] = hue

with open('/home/pi/data/devices/philipsHue.json', 'w') as f:
	json.dump(philipsHueDevices, f)