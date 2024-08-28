#!/usr/bin/env python3
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import time
from pysolar.solar import *
import datetime
import os.path
import sys

import warnings
warnings.filterwarnings("ignore")

VERSION="1.0.0"

from mcpClouds import McpClouds
clouds=McpClouds()
from mcpConfig import McpConfig
config=McpConfig()

# Set up logging
import logging
logFilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mlCloudDetect.log')
logger = logging.getLogger()
fhandler = logging.FileHandler(filename=logFilename, mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.INFO)
logger.info("Program Start - mlCloudDetect"+VERSION)

# Where are the files? 
roofStatusFile='roofStatus.txt'
cloudHistory='cloudHistory.txt'

# Provide usage if no parameters provided
print ("mlCloudDetect by Gord Tulloch gord.tulloch@gmail.com V"+VERSION)
print ("Usage: mlCloudDetect with no parameters. See mlCloudDetect.ini for input parameters")

latestFile=config.get("ALLSKYFILE")

# Set up lat and long so sun altitude can be calc'd
latitude=float(config.get("LATITUDE"))
longitude=float(config.get("LONGITUDE"))

# Set timeframe to set roof operations pending
pendingCount=int(config.get("PENDING"))

#######################################################################################
## DO NOT EDIT FROM HERE ON
#######################################################################################
cloudCount = clearCount = 0
roofStatus="Roof Closed"

while True:
	# If the sun is up don't bother
	date = datetime.datetime.now(datetime.timezone.utc)
	if (get_altitude(latitude, longitude, date) > int(config.get("DAYTIME"))):
		print(date," Daytime skipping")
		f = open(roofStatusFile,"w")	
		f.write("Roof Closed"+"\r\n"+"Daytime")
		f.close()
		time.sleep(60)
		continue
	
	# Call the clouds object to determine if it's cloudy
	result,text=clouds.isCloudy(allSkyOutput=bool(config.get("ALLSKYOUTPUT")))

	if (result):
		cloudCount +=1
		if (cloudCount >= int(config.get("PENDING"))):
			roofStatus=config.get("CLOUDMSG")
			clearCount=0
		elif not(roofStatus==config.get("CLOUDMSG")):
			roofStatus=config.get("CLOUDPENDINGMSG")
			clearCount=0
	else:
		clearCount+=1
		if (clearCount >= int(config.get("PENDING"))):
			roofStatus=config.get("CLEARMSG")
			cloudCount=0
		elif not(roofStatus==config.get("CLEARMSG")):
			cloudCount=0
			roofStatus=config.get("CLEARPENDINGMSG")

	f1=open(roofStatusFile,"w")
	f1.write(roofStatus+"\r\n"+text)
	f1.close
	print(roofStatus," -- ",date,text)

	# Write a log to a weather history file for graphing
	if (config.get("CLOUDHISTORY"=="True")):
		f2=open(cloudHistory,"w")
		f2.write(date.strftime("%m/%d/%Y, %H:%M:%S")+","+result.replace('\n', ''))
		f2.close

	time.sleep(60)
