import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout, MaxPooling2D
import os
import cv2
from PIL import Image
import numpy

# Set up logging
import logging
logFilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mlCloudDetect.log')
logger = logging.getLogger()
fhandler = logging.FileHandler(filename=logFilename, mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)

# Provide usage if no parameters provided
if os.name == 'nt':
	_ = os.system('cls')
else:
	_ = os.system('clear')
print ("trainMlCloudDetect by Gord Tulloch gord.tulloch@gmail.com V1.0 2024/07/17")
print ("Usage: trainMlCloudDetect with no parameters. See mlCloudDetect.ini for input parameters")

VERSION='0.1'

# Set up logging
import logging
logFilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'trainMlCloudDetect.log')
logger = logging.getLogger()
fhandler = logging.FileHandler(filename=logFilename, mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.INFO)
logger.info("Program Start - trainMlCloudDetect"+VERSION)

# Define where the images are. Two sub-dirs are Clear and Cloudy (note caps)
dataDir=config.get('TRAINFOLDER')

# Create the training data from the input folder
trainingDir=dataDir+"Training/"
if not os.path.exists(trainingDir):
        os.makedirs(trainingDir)

# Get a list of classes (folders under trainingDir)
imageClasses = os.listdir(dataDir)
       
for imageClass in imageClasses:
        classDir=trainingDir+imageClass
        if not os.path.exists(classDir):
                os.makedirs(classDir)
        if (imageClass == "Training"):
                continue
        print("Output=",classDir)
        inputDir=dataDir+imageClass+"/"
        print("Input=",inputDir)
        imageFiles = os.listdir(inputDir)
        for image in imageFiles:
                with Image.open(inputDir+image) as img:
                        image_data = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
                thumbnail = cv2.resize(image_data, (224, 224))
                normalized_thumbnail = (thumbnail.astype(numpy.float32) / 127.5) - 1
                #data = numpy.ndarray(shape=(1, 224, 224, 3), dtype=numpy.float32)
                #data[0] = normalized_thumbnail
                normalized_thumbnail.save(classDir+"/"+image)
                
'''
datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
train_generator = datagen.flow_from_directory(
        dataDir,
        target_size=(224, 224),
        batch_size=32,
        shuffle=True,
        class_mode='categorical')
test_generator = datagen.flow_from_directory(
        dataDir,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical')

model1 = Sequential()
model1.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(100,100,3)))
model1.add(Conv2D(32, (3, 3), activation='relu'))
model1.add(MaxPooling2D(pool_size=(2, 2)))
model1.add(Conv2D(64, (3, 3), activation='relu'))
model1.add(Dropout(0.25))
model1.add(Flatten())
model1.add(Dense(128, activation='relu'))
model1.add(Dropout(0.5))
model1.add(Dense(4, activation='softmax'))
model1.compile(loss=tf.keras.losses.categorical_crossentropy,
              optimizer=tf.keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model1.fit(train_generator, epochs=2)
model1.evaluate(test_generator)

model1.save("mlCloudDetect.keras")'''

