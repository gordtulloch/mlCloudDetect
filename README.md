# mlCloudDetect
Cloud Detection using AllSky Cameras. This software will examine images from any allsky camera that can produce an image on disk at a known location. For indi-allsky, the software will load the latest image location from the database. Using Machine Learning, the software compares the most recent image with it's training model to produce a file that will tell you whether the sky is cloudy or clear. For observatories that means open the roof or not. The software also supports pending states where it will delay opening or closing so the observatory isn't constantly opening and closing all night! All messages and configuration is set using an INI file. Also included is a program to train a new model based on your images from your allskycam. Just capture JPG images from your camera into a folder with two sub-folders Clear and Cloudy with the appropriate images in them, and the code will train a new model specific to your sky conditions. This is especially important for dark sky sites where clouds are usually dark, not lit up by lights in my Bortle 8 location.

Requires Python == 3.10 if not using Windows executables.

Releases:
* Version 1.0.1 returns to using a Keras V2 model and thus requires Python 3.10
* Version 1.0.0+ requires a Keras V3 model and will run in any version of Python. It takes no parameters but uses a config file mlCloudDetect.ini (see below). 
* Version 0.9.0 requires Python 3.8 and Keras/Tensorflow 2.11 to support V2 keras model files like those created by Teachable Machine. It requires command line parameters. Run the program without parameters to see usage or see below.

Please see the article at https://openastronomy.substack.com/p/detecting-clouds-with-machine-learning for basic operation and how to create a keras V2 model for your observatory. The primary purpose of the script is to inform weather watcher software whether it's safe and useful to open the observatory roof and commence observations. Note that using the method in this article produces Keras V2 files so you need V0.9.0 of mlCloudDetect.

## Cloud detection model
The mlCloudDetect program requires a Keras format model file to operate. A starter version of this file can be downloaded from the following OneDrive store (it's too big to put on Github)

Keras V2 sample model
* keras_model.h5           https://1drv.ms/u/s!AuTKPznBac46gph4fPUqaRl3XOoHbA?e=GLdplP
* labels.txt               https://1drv.ms/t/s!AuTKPznBac46gph6qOyVBYm_MSSsRw?e=tLrwUA

I suggest that you create your own version of this file as soon as you can since I have trained the model based on images from my Bortle 8 sky, and you will likely have a different sky than mine. See the article above on training your own model with TeachableMachine.

## INI File Parameters
The mlCloudDetect.ini file supports the following parameters:

| Parameter | Default | Description |
|-----------|--------------------------------------------------------|---------------------------------------------------------------------|
| LATITUDE | 49.8954 | Latitude of observer |
| LONGITUDE | -97.1385 | Longitude of observer (negative if West) |
| ALLSKYCAM | INDI-ALLSKY | What kind of allskycam - choice are NONE,INDI-ALLSKY or something else (e.g. TJ) |
| ALLSKYCAMNO | 1 | Determines what camera to pull the latest image from in indi-allsky |
| ALLSKYFILE | /var/www/html/allsky/images/latest.jpg | What the latest file is called (in non-indi-allsky) |
| PENDING | 10 | How long you want to wait to transition between open and closed (in minutes) |
| TRAINFOLDER | /home/stellarmate/allskycam | Folder where training files are |
| CLEARMSG | Roof Open | Message to output when no clouds |
| CLOUDMSG | Roof Closed | Message to output when cloudy |
| CLOUDPENDINGMSG | Close Pending | Message to output when cloud detected but roof open |
| CLEARPENDINGMSG | Open Pending | Message to output when clear sky detected but roof closed |
| KERASMODEL | mlCloudDetect.keras | Model file to use (download from Teachable Machine) |
| KERASLABEL | labels.txt | Labels file for the model (download from Teachable Machine) |
| DAYTIME| -12 | Altitude that the sun has to be at to be full night |

## Installation in Python
To install and run mlCloudDetect in Python, create a Python virtual environment (to avoid various package conflicts) and run the application from a terminal window.

The following instructions are for Ubuntu. You may need to adjust the package names for other Linux distributions. 

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt --assume-yes install python3.10 python3.10-venv 
    git clone https://github.com/gordtulloch/mlCloudDetect.git
    cd mlCloudDetect
    python3.10 -m venv .venv             #
    source .venv/bin/activate        # in Linux, do this every time you run the program to set up the virtual environment
    pip3 install -r requirements.txt
    python3 mlCloudDetect.py

You need to get a jpg named latest.jpg from your allsky software into the mlCloudDetect folder or adjust the path of the program to point to it in the ini file. With the Thomas Joquin software this file is created in /var/www/html/allsky/latest.jpg so edit the mlCloudDetect.py program to find the file there.  In the indi-allsky software mlCloudDetect will query the database for the correct file to analyze as long as it's on the same machine and using the default database option.

## Updating in Python

    cd mlCloudDetect
    git pull
    source .venv/bin/activate
    pip3 install -r requirements.txt 

## Running mlCloudDetect under Windows 
If you don't want to run mlCloudDetect under Python directly there is a Windows version as an exe file created under PyInstaller that incorporates these requirements, so if that works for you please download the exe file from:

Version 1.0.1 
mlCloudDetect.1.0.1.exe []

also required:
* keras_model.h5    https://1drv.ms/u/s!AuTKPznBac46gph4fPUqaRl3XOoHbA?e=GLdplP
* labels.txt        https://1drv.ms/t/s!AuTKPznBac46gph6qOyVBYm_MSSsRw?e=tLrwUA

## Release Log
1.0.1   Minor Upgrade Release 
* Reverts to Keras V2 files produced by TeachableMachine to simplify model production
* Adds Allskycam sampling so every nth image is stored in a folder to facilitate training images
* Logging issues resolved

1.0.0   Milestone release
* Object oriented code
* training of new models to remove version dependency in Tensorflow/Keras using TeachingMachine to generate model
* Labels file not required
* Parameters now stored in INI file
* mlCloudDetect.log includes detailed logging
* Simplified output:
    * Cloud History removed
    * Cloud.txt file removed
    * Allskycam.txt file removed
    * End user configurable output formerly roofStatus.txt
* Windows requirements harmonized with Python

0.9.0   Initial release 
* Parameters to enable use in Windows
* Creates files with roofStatus.txt for whether the roof should be open or not
* allskycam.txt for text to include in allskycam displays
* cloudHistory.txt for cloud history

