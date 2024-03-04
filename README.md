# mlCloudDetect
Cloud Detection using AllSky Cameras

Please see the article at https://openastronomy.substack.com/p/detecting-clouds-with-machine-learning for basic operation and how to create a keras model for your observatory. The primary purpose of the script is to inform weather watcher software whether it's safe and useful to open the observatory roof and commence observations. Runs in Python 3.

Derived from a script provided at https://teachablemachine.withgoogle.com with some additions:
* Determines if the sun is low enough (astronomical twilight) to bother running the model to detect clouds.
* Writes out a status file (clouds.txt) that informs other scripts as to cloud status
* Writes out a status file used by the Allskycam software to display current roof condition
* Writes out a cloudHistory file for later analysis

To install and run mlCloudDetect create a Python virtual environment (to avoid various package conflicts) and run the application from a terminal window.

    python3 -m venv .venv

    source ./venv/bin/activate        # in Linux, do this every time you run the program to set up the virtual environment
    .venv\scripts\activate.bat        # in Windows

    pip3 install -r requirements.txt
    python3 mlCloudDetect.py

You need to get a jpg named latest.jpg from your allsky software into the mlCloudDetect folder or adjust the path of the program to point to it. With the Thomas Joquin software this file is created in /var/www/html/allsky/latest.jpg so edit the mlCloudDetect.py program to find the file there.

In the INDI-Allsky software there's a program in the misc folder that will provide a path to the latest image in the database, so the easiest thing to do is add a line to your crontab (using crontab -e) in Linux as follows to update the image once a minute:

* * * * * cp /var/www/html/allsky/`php /home/user/indi-allsky/makelatest.php` /home/user/mlCloudDetect/latest.jpg