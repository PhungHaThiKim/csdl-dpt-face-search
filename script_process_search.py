import pickle
from typing import List

import cv2
import os
import numpy as np
from sqlalchemy.orm import Session
from tqdm import tqdm

import config
from algorithm.facedetection.facedetect import FaceDetect
from algorithm.featureextraction.featureextract import FeatureExtract

import models
from database import SessionLocal


def search_image_knn(db: Session, path_src):
    img_src = cv2.imread(path_src)
    faces = FaceDetect.faces(img_src)
    faces_crop = FaceDetect.faces_crop(img_src, faces)


    sift_features : List[models.SiftFeature] = db.query(models.SiftFeature).all()

    for facecrop in faces_crop:
        # cv2.imshow("f", facecrop)
        # cv2.waitKey(0)
        key, des_src = FeatureExtract.sift(facecrop)
        lenkey_src = len(key)
        for sift in sift_features:
            path_dist = os.path.join(config.DATA_PATH, sift.sift_feature_path)
            with open(path_dist, 'rb') as file:
                lenkey_dist, des_dist = pickle.load(file)

            if lenkey_src > 2 and lenkey_dist > 2:
                flann = cv2.FlannBasedMatcher_create()
                matches = flann.knnMatch(des_src, des_dist, k=2)
                good_points = []
                number_keypoints = 0
                for m, n in matches:
                    if m.distance < 0.55 * n.distance:
                        good_points.append(m)
                    if lenkey_src <= lenkey_dist:
                        number_keypoints = lenkey_src
                    else:
                        number_keypoints = lenkey_dist

                if len(good_points) / number_keypoints * 100 >= 10:
                    print(sift.face.frame.frame_path, len(good_points) / number_keypoints * 100, "%")

                    # face_path = os.path.join(config.DATA_PATH, sift.face.face_path)
                    # faceread = cv2.imread(face_path)
                    # cv2.imshow("f2", faceread)
                    # cv2.waitKey(0)

def search_image_euclidean(db: Session, path_src):
    img_src = cv2.imread(path_src)
    faces = FaceDetect.faces(img_src)
    faces_crop = FaceDetect.faces_crop(img_src, faces)


    lbp_features : List[models.LbpFeature] = db.query(models.LbpFeature).all()

    for facecrop in faces_crop:

        # cv2.imshow("face", facecrop)
        # cv2.waitKey(0)

        lbp_src = FeatureExtract.local_binary_pattern(facecrop)

        # cv2.imshow("lbp", lbp_src)
        # cv2.waitKey(0)

        for lbp in lbp_features:
            path_dist = os.path.join(config.DATA_PATH, lbp.lbp_feature_path)
            with open(path_dist, 'rb') as file:
                lbp_dist = pickle.load(file)

                dist = np.sqrt(np.nansum(np.square(lbp_src - lbp_dist)))

                print(lbp.face.frame.frame_path, dist)
                if dist <= 50:
                    print("ok", lbp.face.frame.frame_path, dist)


if __name__ == "__main__":
    image_search_path = "E:\\Banggioi\\Ky8\\CSDL DPT\\code\\csdl-dpt-face-search\\search\\ronaldo.png"

    db: Session = SessionLocal()
    search_image_euclidean(db, image_search_path)
    db.close()

