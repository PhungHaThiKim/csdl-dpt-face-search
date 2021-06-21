import pickle
from typing import List

import os
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from tqdm import tqdm

import config
from algorithm.facedetection.facedetect import FaceDetect
from algorithm.featureextraction.featureextract import FeatureExtract
import cv2 as cv

import models
from database import SessionLocal

def search_image_euclidean(db: Session, img_src):

    rs = []
    # Tach cac face tu anh dau vao
    faces = FaceDetect.faces(img_src)
    # Cat cac face
    faces_crop = FaceDetect.faces_crop(img_src, faces)

    # Lay ds tat ca cac lbp_feature tu db
    lbp_features: List[models.LbpFeature] = db.query(models.LbpFeature).all()

    # duyet tung face
    for facecrop in faces_crop:

        cv.imwrite("Face.png", facecrop)
        # local_binary_pattern tren moi face
        lbp_src = FeatureExtract.local_binary_pattern(facecrop)
        cv.imwrite("LBP.png", lbp_src)

        # histogram anh xam local_binary_pattern
        lbp_src = FeatureExtract.histogram_bit(lbp_src)
        plt.plot(lbp_src)
        plt.show()
        plt.imsave("plot.png")

        lbp_src = lbp_src/np.nansum(lbp_src)

        # so sanh feature anh dau vao voi tung cac feature da co
        for lbp in lbp_features:
            path_dist = os.path.join(config.DATA_PATH, lbp.lbp_feature_path)
            #Load feature tu folder vat ly
            with open(path_dist, 'r') as file:
                lbp_dist = np.loadtxt(file)
                lbp_dist = lbp_dist/np.nansum(lbp_dist)
                #So sanh theo khoang cach khoảng cách Euclid
                dist = np.sqrt(np.nansum(np.square(lbp_src - lbp_dist)))

                print(lbp.face.frame.frame_path, dist)

                # Xet nguong khoang cach de lua chon face/frame/shot/video chuan nhat
                if dist <= 0.04:
                    print("ok", lbp.face.frame.frame_path, dist)
                    rs.append({
                        "lbp": lbp,
                        "dist": dist
                    })

    #Sort uu tien khoang cach gan nhat
    rs.sort(key=lambda t: t["dist"])

    return rs, faces_crop


if __name__ == "__main__":
    image_search_path = "E:\\Banggioi\\Ky8\\CSDL DPT\\code\\csdl-dpt-face-search\\search\\ronaldo2.png"
    img_src = cv.imread(image_search_path)
    db: Session = SessionLocal()
    search_image_euclidean(db, img_src)
    db.close()

