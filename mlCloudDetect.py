from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import time
from pysolar.solar import *
import datetime

# Set up lat and long so sun altitude can be calc'd
latitude=49.9
longitude=-97.1

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

while True:
	# If the sun is up don't bother
	date = datetime.datetime.now(datetime.timezone.utc)
	if (get_altitude(latitude, longitude, date) > -6.0):
		print("Daytime skipping")
		f = open("status.txt","w")
		f.write("Daytime")
		f.close()
		time.sleep(60)
		continue
	
	# Replace this with the path to your image
	image = Image.open("latest.jpg").convert("RGB")

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

	# Print prediction and confidence score
	f=open("status.txt","w")
	f.write(class_name[2:].replace('\n', '')+" ("+confidence_score.astype('str')+")")
	f.close

	time.sleep(60)
