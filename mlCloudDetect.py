from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import time
from pysolar.solar import *
import datetime
import os.path
import smtplib
from email.mime.text import MIMEText

# Set up email send
def send_email(subject, body, sender, recipients, password):
	msg = MIMEText(body)
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = ', '.join(recipients)
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
		smtp_server.login(sender, password)
		smtp_server.sendmail(sender, recipients, msg.as_string())

def notifyUser(roofStatus):
	# If status has changed send a text to the user
	subject = "SPAO Roof Status Change"
	body = roofStatus
	sender = "spao@gmail.com"
	#recipients = ["user@gmail.com"]
	recipients = ["user@gmail.com"]
	password = ""
	send_email(subject, body, sender, recipients, password)
	lastRoofStatus = roofStatus

# Where are the files? The commented files are where I normally run them for INDI Weather Watcher etc. EDIT THIS
latestFile='latest.jpg'
#cloudsFile='/usr/local/share/indi/scripts/clouds.txt'
cloudsFile='clouds.txt'
#roofFile='/usr/local/share/indi/scripts/roofStatus.txt'
roofFile='roofStatus.txt'
#roofStatusFile="/usr/local/share/indi/scripts/roofStatus.txt"
roofStatusFile='roofStatus.txt'
cloudHistory='/usr/local/share/indi/scripts/cloudHistory.txt'

# Set up lat and long so sun altitude can be calc'd EDIT THIS
latitude=49.9
longitude=-97.1

#######################################################################################
## DO NOT EDIT FROM HERE ON
#######################################################################################
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

cloudCount = clearCount = 0
roofStatus="Roof Closed"

while True:
	# If the sun is up don't bother
	date = datetime.datetime.now(datetime.timezone.utc)
	if (get_altitude(latitude, longitude, date) > -12.0):
		print(date," Daytime skipping")
		f = open(cloudsFile,"w")
		f.write("Daytime")
		f.close()
		f = open(roofStatusFile,"w")	
		f.write("Roof Closed")
		f.close()
		time.sleep(60)
		continue
	
	# Replace this with the path to your image
	image = Image.open(latestFile).convert("RGB")

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
	prediction = model.predict(data)
	index = np.argmax(prediction)
	class_name = class_names[index]
	confidence_score = prediction[0][index]

	# Update cloud status file
	f=open(cloudsFile,"w")
	f.write(class_name[2:].replace('\n', '')+" ("+confidence_score.astype('str')+")")
	f.close

	# If there is a SAFEMODE then we're closed
	#if (os.path.isfile("/usr/local/share/indi/scripts/SAFEMODE")):
	#	roofStatus="Roof Closed"
	#	f.write(roofStatus)
	#	f.close
	#	continue

	# Otherwise update Roof status
	if (class_name[2:].replace('\n', '')!="Clear"):
		cloudCount +=1
		if (cloudCount>=10):
			roofStatus="Roof Closed"
			clearCount=0
		elif (cloudCount < 10) and not(roofStatus=="Roof Closed"):
			roofStatus="Close Pending"
			clearCount=0
	else:
		clearCount+=1
		if (clearCount>=10):
			roofStatus="Roof Open"
			cloudCount=0
		elif (clearCount>0) and not(roofStatus=="Roof Open"):
			cloudCount=0
			roofStatus="Open Pending"

	f1=open(roofFile,"w")
	f1.write(roofStatus+"\r\n"+class_name[2:].replace('\n', ''))
	f1.close
	print(roofStatus," -- ",date,class_name[2:].replace('\n', '')+" ("+confidence_score.astype('str')+")")

	# Write a log to a weather history file for graphing
	f2=open(cloudHistory,"w")
	f2.write(date.strftime("%m/%d/%Y, %H:%M:%S")+","+class_name[2:].replace('\n', ''))
	f2.close

	time.sleep(60)
