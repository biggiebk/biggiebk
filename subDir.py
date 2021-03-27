#!/usr/bin/python3
from numpy import random
import os
import sys
rootDir = "/home/pi/Music/%s" %(sys.argv[1])
directory = random.choice(os.listdir(rootDir))
media = random.choice(os.listdir("%s/%s" %(rootDir, directory)))
print("%s/%s/%s" %(rootDir, directory, media))