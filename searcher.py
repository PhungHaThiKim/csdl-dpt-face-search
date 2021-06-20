import cv2
import os
import numpy as np
from algorithm.facedetection.facedetect import FaceDetect
from algorithm.featureextraction.featureextract import FeatureExtract
from scipy.spatial import distance
from scipy.spatial.distance import euclidean

img = cv2.imread('./search/4.png')
faces = FaceDetect.faces(img)
img_faces = FaceDetect.faces_crop(img, faces)
print(img_faces.shape)

# colors = os.listdir('./data/001/faces')
# colors_path = [os.path.abspath('./data/001/faces/'+f) for f in colors if os.path.isfile(os.path.join('./data/001/faces', f))]

colors = os.listdir('./data/001/faces')
colors_path = [os.path.abspath('./data/001/faces/'+f) for f in colors if os.path.isfile(os.path.join('./data/001/faces', f))]

print(colors_path)

fcolors = []
for cp in colors_path:
    # fcolors.append(np.load(cp))
    fcolors.append(cv2.imread(cp))
fcolors = np.array(fcolors)
print(fcolors.shape)

for i in range(img_faces.shape[0]):
    imface = img_faces[i]
    # fface = FeatureExtract.histogram_color(imface)
    # fface = FeatureExtract.local_binary_pattern(imface)
    # print(fface.shape)
    # fface = FeatureExtract.histogram_bit(fface)
    # print(fface.shape)

    key1, des1 = FeatureExtract.sift(imface)


    # cv2.imshow('frame', fface)
    # #
    # cv2.waitKey(0)

    for j in range(fcolors.shape[0]):
        fcolor = fcolors[j]
        # fcolor = FeatureExtract.local_binary_pattern(fcolor)
        # fcolor = FeatureExtract.histogram_bit(fcolor)
        # print(fcolor.shape)
        # dist = cv2.compareHist(fface, fcolor, cv2.HISTCMP_CHISQR)
        # dist = distance.hamming(imface.flatten(), fcolor.flatten())
        # dist = euclidean(fface, fcolor)

        key2, des2 = FeatureExtract.sift(fcolor)
        # bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
        # matches = bf.match(des1, des2)
        if len(key1) > 2 and len(key2) > 2:
            index_params = dict(algorithm=0, trees=5)
            search_params = dict()
            flann = cv2.FlannBasedMatcher_create()
            matches = flann.knnMatch(des1, des2, k=2)
            good_points = []
            for m, n in matches:
                if m.distance < 0.55*n.distance:
                    good_points.append(m)

            number_keypoints = 0
            if len(key1) <= len(key2):
                number_keypoints = len(key1)
            else:
                number_keypoints = len(key2)
            print(colors_path[j], len(good_points) / number_keypoints * 100, "%")


        # print("Distance:", colors_path[j], dist)

# cv2.destroyAllWindows()

