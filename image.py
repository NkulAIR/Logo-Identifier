import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

# Load the pre-trained ResNet50 model
model = ResNet50(weights='imagenet')

# Path to the input image
img_path = 'soccer.jpg'  # Ensure this image exists in the working directory

# Load the image
img = cv2.imread(img_path)
if img is None:
    raise FileNotFoundError(f"Image {img_path} not found or could not be loaded.")

# Convert BGR to RGB
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Preprocess the image
img = cv2.resize(img, (224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# Make predictions
preds = model.predict(x)

# Decode and display predictions
print('Predicted:', decode_predictions(preds, top=3)[0])
