import dlib
import torch
import cv2 as cv2
import numpy as np
from numpy import load
from numpy import asarray
from numpy import expand_dims
from numpy import savez_compressed
from plot_utils import resize_image
from tensorflow.python.keras.models import load_model
import matplotlib.pyplot as plt

import h5py

# import warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)

class FaceDetection:

    def __init__(self):
        model_file = "models/res10_300x300_ssd_iter_140000.caffemodel"
        config_file = "models/deploy.prototxt.txt"
        self.net =  cv2.dnn.readNetFromCaffe(config_file, model_file)
        self.model = load_model("./models/facenet_keras.h5", compile=False)
        
    # Returns an array of bounding boxes of human faces in a image
    def get_face_locations_with_dnn(self, rgb_small_frame, confidence_threshold = 0.95):

        face_locations = []
        image_height, image_width = rgb_small_frame.shape[:2]
        resized_image = cv2.resize(rgb_small_frame, (300, 300))
        blob = cv2.dnn.blobFromImage(resized_image, 1.0,(300, 300), (104.0, 117.0, 123.0))
        self.net.setInput(blob)
        faces = self.net.forward()

        # Our next step is to loop over all the co-ordinates it returned and draw rectangles around them using Open CV.
        # We will be drawing a green rectangle with thicknes
        for i in range(faces.shape[2]):

                # extract the confidence (i.e., probability) associated with the prediction
                confidence = faces[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is greater than the minimum confidence
                if confidence > confidence_threshold:

                    # compute the (x, y)-coordinates of the bounding box for the object
                    box = faces[0, 0, i, 3:7] * np.array([image_width, image_height, image_width, image_height])
                    (x, y, x1, y1) = box.astype("int")

                    face_locations.append(box.astype("int"))

        return face_locations

    # Given an face image, return the 128-dimension face encoding
    def get_face_encodings(self,rgb_small_frame, box):

        x1, y1, x2, y2 = box

        face = rgb_small_frame[int(y1):int(y2), int(x1):int(x2)]

        if(face.shape[0] < 160 or face.shape[1] < 160):
            return None

        face = cv2.resize(face, (160, 160), interpolation = cv2.INTER_AREA)

        face_pixels = asarray(face)
        
        # scale pixel values
        face_pixels = face_pixels.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        # transform face into one sample
        samples = expand_dims(face_pixels, axis=0)
        # make prediction to get embedding
        yhat = self.model.predict(samples)
        return yhat[0]
    
    def detect_faces(self, small_frame, path, confidence_threshold = 0.95):
        # Resize frame of video to 1/3 size for faster face recognition processing
        # small_frame = resize_image(small_frame)

        # Find all the faces and face encodings in the current image
        face_locations = self.get_face_locations_with_dnn(small_frame, confidence_threshold)
        
        faces = []

        for face_location in face_locations:

            face_encoding = self.get_face_encodings(small_frame, face_location)

            if face_encoding is None:
                continue

            face = {
                "face_encoding": face_encoding,
                "face_location": face_location,
                "image_path": path
            }

            # Grab a single frame of video
            faces.append(face)
            
        return faces