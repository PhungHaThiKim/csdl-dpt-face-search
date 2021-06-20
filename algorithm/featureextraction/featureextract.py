import cv2
import cv2 as cv
from skimage.feature import local_binary_pattern
import numpy as np

class FeatureExtract:
    @staticmethod
    def histogram_color(img):
        hsv1 = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        hist1 = cv.calcHist([hsv1], [0, 1], None, [180, 256], [0, 180, 0, 256])
        cv.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
        return hist1

    @staticmethod
    def histogram_bit(img):
        hist, _ = np.histogram(img, bins=np.arange(2**8 + 1), density=True)
        return hist

    @staticmethod
    def local_binary_pattern(img):
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        lbp = local_binary_pattern(img, 8, 1, method="uniform")
        return lbp

    @staticmethod
    def sift(img):
        img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sift = cv2.SIFT_create()
        keypoints_1, descriptors_1 = sift.detectAndCompute(img1, None)
        return keypoints_1, descriptors_1