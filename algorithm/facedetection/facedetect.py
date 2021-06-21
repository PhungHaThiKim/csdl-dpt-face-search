import os

import numpy as np
import cv2
from algorithm.featureextraction.featureextract import FeatureExtract

class FaceDetect:
    PREFIX = "E:\\Banggioi\\Ky8\\CSDL DPT\\code\\csdl-dpt-face-search\\venv\\Lib\\site-packages\\cv2\\data"

    @staticmethod
    def faces(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(FaceDetect.PREFIX+'/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        # print(len(faces))
        return faces

    @staticmethod
    def faces_crop(img, faces):
        rs = []
        for (x, y, w, h) in faces:
            crop = img[y:y + h, x:x + w]
            crop = cv2.resize(crop, (300, 300))
            rs.append(crop)
        return np.array(rs)

if __name__ == "__main__":
    frames = os.listdir('../../data/001/frames')
    print(frames)
    frames = [os.path.abspath('../../data/001/frames/'+f) for f in frames if os.path.isfile(os.path.join('../../data/001/frames', f))]
    print(frames)
    stt = 0
    for fr in frames:
        img = cv2.imread(fr)
        faces = FaceDetect.faces(img)
        for (x, y, w, h) in faces:
            crop = img[y:y+h, x:x+w]
            filename = "{}.png".format(stt+1)
            filepath = os.path.abspath('../../data/001/faces/'+filename)
            crop = cv2.resize(crop, (300, 300))
            cv2.imwrite(filepath, crop)
            print("Save:", filepath)
            # color_feature = FeatureExtract.histogram_color(crop)
            # with open('../../data/001/features/color/'+"{}.npy".format(stt+1), 'wb') as fi:
            #     np.save(fi, color_feature)
            lbp_feature = FeatureExtract.local_binary_pattern(crop)
            with open('../../data/001/features/texture/' + "{}.npy".format(stt + 1), 'wb') as fi:
                np.save(fi, lbp_feature)
            print(lbp_feature.shape)
            stt += 1