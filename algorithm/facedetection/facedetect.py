import os

import numpy as np
import cv2

import config
from algorithm.featureextraction.featureextract import FeatureExtract

class FaceDetect:
    PREFIX = config.CASCADE_PATH

    @staticmethod
    def faces(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Load cac window dac trung kieu Haar
        face_cascade = cv2.CascadeClassifier(FaceDetect.PREFIX+'/haarcascade_frontalface_default.xml')
        # Detect cac face tren anh
        faces = face_cascade.detectMultiScale(gray, 1.3, 9, minSize=(30, 30))
        return faces

    @staticmethod
    def faces_crop(img, faces):
        rs = []
        # Cat face
        for (x, y, w, h) in faces:
            crop = img[y:y + h, x:x + w]
            crop = cv2.resize(crop, (300, 300))
            rs.append(crop)
        return np.array(rs)

if __name__ == "__main__":

    pass