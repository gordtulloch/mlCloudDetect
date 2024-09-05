import sys
import argparse
from pathlib import Path
import time
from datetime import datetime
from datetime import timedelta
import numpy as np
import cv2
import PIL
from PIL import Image
import logging
import sqlite3
import os

from mcpConfig import McpConfig
config=McpConfig()

logger = logging.getLogger("mcpClouds")

# Suppress Tensorflow warnings
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import keras
logger.setLevel(logging.INFO)

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

    def isCloudy(self,allSkyOutput=False):
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

        result=self.detect(image_file)

        return (result != 'Clear',result.replace('\n', ''))

    def detect(self, imagePath):
        # Load and preprocess the image
        image = Image.open(imagePath)
        image = image.resize((256, 256))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        detect_start = time.time()

        # Predicts the model
        prediction = self.model.predict(image_array)
        idx = np.argmax(prediction)
        class_name = self.CLASS_NAMES[idx]
        confidence_score = (prediction[0][idx]).astype(np.float32)

        detect_elapsed_s = time.time() - detect_start
        logger.info('Cloud detection in %0.4f s', detect_elapsed_s)
        logger.info('Rating: %s, Confidence %0.3f', class_name, confidence_score)
        
        return(class_name)

