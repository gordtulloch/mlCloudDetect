# mlCloudDetect
Cloud Detection using AllSky Cameras

Please see the article at https://openastronomy.substack.com/p/detecting-clouds-with-machine-learning for basic operation and how to create a keras model for your observatory. The primary purpose of the script is to inform weather watcher software whether it's safe and useful to open the observatory roof and commence observations.

Derived from a script provided at https://teachablemachine.withgoogle.com with some additions:
* Determines if the sun is low enough (astronomical twilight) to bother running the model to detect clouds.
* Writes out a status file (clouds.txt) that informs other scripts as to cloud status
* Writes out a status file used by the Allskycam software to display current roof condition
