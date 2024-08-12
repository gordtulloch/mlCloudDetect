#############################################################################################################
## C O N F I G                                                                                       ##
#############################################################################################################
# Object to retrieve configuration
import configparser
import os
import logging
logger = logging.getLogger('mcpConfig')

class McpConfig():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mlCloudDetect.ini')
        # Check if the file exists
        if not os.path.exists(self.file_path):
            logger.info("Config file not found, creating with defaults.")
            self.config['DEFAULT'] = {
                'LATITUDE'      : '49.8954',            # Latitude of observer
                'LONGITUDE'     : '-97.1385',           # Longitude of observer
                'ALLSKYCAM'     : 'INDI-ALLSKY',        # What kind of allskycam - choice are NONE,INDI-ALLSKY or something else (e.g. TJ)
                'ALLSKYCAMNO'   : '1',                  # Determines what camera to pull the latest image from in indi-allsky
                'ALLSKYFILE'    : 'latest.jpg',         # What the latest file is called (in non-indi-allsky)
                'ALLSKYOUTPUT'  : 'True',               # Dump an allskycam.txt file with cloud status
                'PENDING'       : 10,                   # How long you want to wait to transition between open and closed (in minutes)
            }
            with open(self.file_path, 'w') as configfile:
                self.config.write(configfile)
                return      
    def get(self,keyword):
                self.config = configparser.ConfigParser()
                self.config.read(self.file_path)
                return self.config['DEFAULT'][keyword]

