# mlCloudDetect
Cloud Detection using AllSky Cameras

Releases:
* Version 1.0.0+ requires a Keras V3 model and will run in any version of Python. It takes no parameters but uses a config file mlCloudDetect.ini (see below). 
* Version 0.9.0 requires Python 3.8 and Keras/Tensorflow 2.11 to support V2 keras model files like those created by Teachable Machine. It requires command line parameters. Run the program without parameters to see usage or see below.

Please see the article at https://openastronomy.substack.com/p/detecting-clouds-with-machine-learning for basic operation and how to create a keras V2 model for your observatory. The primary purpose of the script is to inform weather watcher software whether it's safe and useful to open the observatory roof and commence observations. Note that using the method in this article produces Keras V2 files so you need V0.9.0 of mlCloudDetect.

## Cloud detection model
The mlCloudDetect program requires a Keras format model file to operate. A starter version of this file can be downloaded from the following OneDrive store (it's too big to put on Github)

Keras V3 sample model 
* mlCloudDetect.keras     https://1drv.ms/u/s!AuTKPznBac46gph3tMCqR540AAZUfg?e=LJXvH6

Keras V2 sample model (for the old version 0.9.0)
* keras_model.h5           https://1drv.ms/u/s!AuTKPznBac46gph4fPUqaRl3XOoHbA?e=GLdplP
* labels.txt               https://1drv.ms/t/s!AuTKPznBac46gph6qOyVBYm_MSSsRw?e=tLrwUA

I suggest that you create your own version of this file as soon as you can since I have trained the model based on images from my Bortle 8 sky, and you will likely have a different sky than mine. To train a new model:

* Capture sample images from your All Sky Camera and put them into a training folder with two sub-folders - Clear and Cloudy
* Back up your existing mlCloudDetect.keras file somewhere safe.
* Update mlCloudDetect.ini to set trainfolder to the location of your image folders e.g. C:/Users/myuser/Desktop/allskyimages/ (note the forward slashes if you are running Windows!)
* Run the program trainMlCloudDetect.py (or the EXE file in Windows) which will create a new mlCloudDetect.keras file for you

## Version 0.9.0 Parameters (SUPERCEDED)
This version of the program was modified to run as a Windows exe so all of the previously editable parameters in the script were made command line parameters. needs to be called with the following:

    mlCloudDetect lat long pending imagefile

where lat and long are your latitude and longitude, pending is the number of minutes you want to delay between opening and closing your roof, and imagefile is the latest image file for your allsky cam.So for example at my location:

    mlCloudDetect 49.9 -97.1 10 latest.jpg

Version 1.0.0+ of the program moved all parameters into an INI file. 

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
| KERASMODEL | mlCloudDetect.keras | Model file to use |
| DAYTIME| -12 | Altitude that the sun has to be at to be full night |

## Installation in Python
To install and run mlCloudDetect in Python, create a Python virtual environment (to avoid various package conflicts) and run the application from a terminal window.

    git clone https://github.com/gordtulloch/mlCloudDetect.git
    cd mlCloudDetect
    python3 -m venv .venv             # Note that if the correct Python version is not the only one installed you should specify the version eg python3.8
    source .venv/bin/activate        # in Linux, do this every time you run the program to set up the virtual environment
    .venv\scripts\activate.bat        # in Windows

    pip3 install -r requirements.txt
    python3 mlCloudDetect.py

You need to get a jpg named latest.jpg from your allsky software into the mlCloudDetect folder or adjust the path of the program to point to it in the ini file. With the Thomas Joquin software this file is created in /var/www/html/allsky/latest.jpg so edit the mlCloudDetect.py program to find the file there.  In the indi-allsky software mlCloudDetect will query the database for the correct file to analyze.

## Updating in Python

    cd mlCloudDetect
    git pull

## Running mlCloudDetect under Windows 
If you don't want to run mlCloudDetect under Python directly there is a Windows version as an exe file created under PyInstaller that incorporates these requirements, so if that works for you please download the exe file from:

Version 0.9.0 (old Keras V2 model files)
mlCloudDetect.0.9.0.exe [https://1drv.ms/u/s!AuTKPznBac46gphDwGPjozIPB4FvVw?e=EClepg](https://1drv.ms/u/s!AuTKPznBac46gphDwGPjozIPB4FvVw?e=kAGErY)

also required:
* keras_model.h5    https://1drv.ms/u/s!AuTKPznBac46gph4fPUqaRl3XOoHbA?e=GLdplP
* labels.txt        https://1drv.ms/t/s!AuTKPznBac46gph6qOyVBYm_MSSsRw?e=tLrwUA

Version 1.0.0
mlCloudDetect.1.0.0             https://1drv.ms/u/s!AuTKPznBac46gph_50chTGj1dKS1Nw?e=DCnptR
trainMlCloudDetect.1.0.0.exe    https://1drv.ms/u/s!AuTKPznBac46gpkA_zD36PS0xB8OpQ?e=pzdUrZ

## Release Log
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

