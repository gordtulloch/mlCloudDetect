import keras
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps  # Install pillow instead of PIL
import sqlite3
import shutil
import os
import datetime
import paho.mqtt.client as mqtt

from mcpConfig import McpConfig
config=McpConfig()

import logging
logger = logging.getLogger("mcpClouds")

sys.path.append(str(Path(__file__).parent.absolute().parent))

# OO version derived from indi-allsky by Aaron Morris https://github.com/aaronwmorris/indi-allsky.git thanks Aaron!
# Original derived from Google Teaching Machine output

class McpClouds(object):
    CLASS_NAMES = (
        'Clear',
        'Cloudy',
    )
    
    def __init__(self):
        self.config = config
        logger.info('Using keras model: %s', config.get("KERASMODEL"))
        self.model = keras.models.load_model(config.get("KERASMODEL"), compile=False)
        if self.config.get("ALLSKYSAMPLING")=="True":
            if not os.path.exists(self.config.get("ALLSKYSAMPLEDIR")):
                os.makedirs(self.config.get("ALLSKYSAMPLEDIR"))
            for className in self.CLASS_NAMES:
                if not os.path.exists(self.config.get("ALLSKYSAMPLEDIR")+"/"+className):
                    os.makedirs(self.config.get("ALLSKYSAMPLEDIR")+"/"+className)
            self.imageCount=1
            if self.config.get("MQTT_ENABLE") == "True":
                logger.info('Enabling MQTT')
                try:
                    self.mqttClient = mqtt.Client()
                    self.mqttClient.connect(self.config.get("MQTT_BROKER"), int(self.config.get("MQTT_PORT")), 60)
                    self.mqttClient.loop_start()
                except Exception as e:
                    logger.error('Error connecting to MQTT: %s', e)

    def isCloudy(self):
        if (self.config.get("ALLSKYCAM") == "NONE"):
            logger.error('No allsky camera for cloud detection')
            print('ERROR: No allsky camera for cloud detection, exiting')
            exit(0)
        else:
            if (self.config.get("ALLSKYCAM") == "INDI-ALLSKY"):
                # Query the database for the latest file
                try:
                    conn = sqlite3.connect('/var/lib/indi-allsky/indi-allsky.sqlite')
                    cur = conn.cursor()
                    sqlStmt='SELECT image.filename AS image_filename FROM image ' + \
                    'JOIN camera ON camera.id = image.camera_id WHERE camera.id = '+ self.config.get("ALLSKYCAMNO") +\
                    ' ORDER BY image.createDate DESC LIMIT 1'
                    logger.info('Running SQL Statement: '+sqlStmt)
                    cur.execute(sqlStmt)
                    image_file='/var/www/html/allsky/images/'+cur.fetchone()[0]
                    conn.close()
                except sqlite3.Error as e:
                    logger.error("SQLITE Error accessing indi-allsky "+str(e))
                    print("SQLITE Error accessing indi-allsky "+str(e)+", exiting")
                    exit(0)
            else:
                # Grab the image file from whereever 
                image_file = config.get("ALLSKYFILE")
        logger.info('Loading image: %s', image_file)
        
        result=self.detect(image_file).replace('\n', '')

        # Publish to MQTT if enabled
        if self.config.get("MQTT_ENABLE") == "True":
            logger.info('Publishing to MQTT')
            try:
                self.mqttClient.publish(self.config.get("MQTT_TOPIC"), result)
            except Exception as e:
                logger.error('Error publishing to MQTT: %s', e)
                
        # If allskysampling turned on save a copy of the image if count = allskysamplerate
        if self.config.get("ALLSKYSAMPLING") == "True":
            logging.info('Sampling image count ' + str(self.imageCount))
            if self.imageCount == int(self.config.get("ALLSKYSAMPLERATE")):
                # Get the current date and time
                current_datetime = datetime.datetime.now()
                # Format the date and time as a string
                date_str = current_datetime.strftime("%Y%m%d_%H%M%S")
                # Create a filename with the current date
                filename = f"image_{date_str}.jpg"
                destination_path = self.config.get('ALLSKYSAMPLEDIR')+"/"+result+"/"+filename
                shutil.copy(image_file, destination_path)
                logging.info(f"Copying {image_file} to {destination_path}")
                self.imageCount = 1
            else:
                self.imageCount += 1    

        return (result != 'Clear',result)

    def detect(self, imagePath):
         # Load the labels
        class_names = open(config.get("KERASLABEL"), "r").readlines()

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Replace this with the path to your image
        image = Image.open(config.get("ALLSKYFILE")).convert("RGB")

        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # Predicts the model
        prediction = self.model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        logger.info("Class:"+str(class_name[2:]).replace('\n', ''))
        logger.info("Confidence Score:"+str(confidence_score))

        return(class_name[2:])

