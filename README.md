# mlCloudDetect
Cloud Detection using AllSky Cameras

Releases:
* Version 0.9.0 requires Python 3.8 and Keras/Tensorflow 2.11 to support V2 keras model files like those created by Teachable Machine. It requires command line parameters. Run the program without parameters to see usage or see below.
* Version 1.0.0 (in development) will include a Keras V3 model generation script and will run in any version of Python. It takes no parameters but uses a config file mlCloudDetect.ini.

Please see the article at https://openastronomy.substack.com/p/detecting-clouds-with-machine-learning for basic operation and how to create a keras model for your observatory. The primary purpose of the script is to inform weather watcher software whether it's safe and useful to open the observatory roof and commence observations. 
Please see the article at https://openastronomy.substack.com/p/detecting-clouds-with-machine-learning for basic operation and how to create a keras model for your observatory. The primary purpose of the script is to inform weather watcher software whether it's safe and useful to open the observatory roof and commence observations. Runs in Python 3.8 currently as it requires Keras and Tensorflow 2.11 for the V2 Keras model produced by Teachable Machine. V1.0.0 (in development) will include a training script to solve this issue.

Derived from a script provided at https://teachablemachine.withgoogle.com with some additions:
* Determines if the sun is low enough (astronomical twilight) to bother running the model to detect clouds.
* Writes out a status file (clouds.txt) that informs other scripts as to cloud status
* Writes out a status file (roofStatus.txt) used by the Allskycam software to display current roof condition
* Writes out a cloudHistory file for later analysis (cloudHistory.txt)

## Version 0.9.0 Parameters
The code was recently modified to run as a Windows exe so all of the previously editable parameters in the script were made command line parameters. needs to be called with the following:

mlCloudDetect <lat> <long> <pending> <imagefile>

where lat and long are your latitude and longitude, pending is the number of minutes you want to delay between opening and closing your roof, and imagefile is the latest image file for your allsky cam.So for example at my location:

mlCloudDetect 49.9 -97.1 10 latest.jpg

## Virtual Environments
To install and run mlCloudDetect in Python create a Python virtual environment (to avoid various package conflicts) and run the application from a terminal window.

    python3 -m venv .venv             # Note that if the correct Python version is not the only one installed you should specify the version eg python3.8
    source ./venv/bin/activate        # in Linux, do this every time you run the program to set up the virtual environment
    .venv\scripts\activate.bat        # in Windows

    pip3 install -r requirements.txt
    python3 mlCloudDetect 49.9 -97.1 10 latest.jpg

You need to get a jpg named latest.jpg from your allsky software into the mlCloudDetect folder or adjust the path of the program to point to it. With the Thomas Joquin software this file is created in /var/www/html/allsky/latest.jpg so edit the mlCloudDetect.py program to find the file there.

In the INDI-Allsky software there's a program in the misc folder that will provide a path to the latest image in the database, so the easiest thing to do is add a line to your crontab (using crontab -e) in Linux as follows to update the image once a minute:
    * * * * * cp /var/www/html/allsky/`php /home/user/indi-allsky/makelatest.php` /home/user/mlCloudDetect/latest.jpg

## Running mlCloudDetect under Windows
There are issues with Tensorflow and Keras on Windows in current versions of Python as of this writing (version 3.12.4) so running under Windows requires a previous version of Python. Version 3.8.x has been testing using Tensorflow 3.11. There has been an exe file created under PyInstaller that incorporates these requirements, so if that works for you please download the exe file from:

https://1drv.ms/u/s!AuTKPznBac46gphDwGPjozIPB4FvVw?e=EClepg

You just need to stick the keras model and labels files in the same folder and run it.

## Setting mlCloudDetect as a Linux service
To set up mlCloudDetect as a service, ensure the mlCloudDetect file is executable and install the following file into the folder ~/.config/systemd/user/cloudDetect.service:

    [Unit]
    Description=Cloud Detection Service
    After=network.target indiserver.service indi-allsky.service
 
    [Service]
    WorkingDirectory=/home/<user>/CloudDetect
    ExecStart=/home/gtulloch/CloudDetect/mlCloudDetect.py >> /home/<user>>/CloudDetect/mlCloudDetect.log 2>>&1 
    ExecReload=/bin/kill -HUP $MAINPID
    ExecStop=/bin/kill -TERM $MAINPID
    Restart=always
    user=youraccount
    PrivateTmp=true
    UMask=0022

    [Install]
    WantedBy=multi-user.target

to enable execute the following commands:

    $ systemctl --user enable cloudDetect
    $ systemctl --user start cloudDetect
    $ systemctl --user start cloudDetect

Stop the service with:

    $ systemctl --user stop cloudDetect

    



