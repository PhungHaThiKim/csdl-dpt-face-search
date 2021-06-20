import cv2
import cv2 as cv
import numpy as np
from scipy.stats import wasserstein_distance

class SceneDetection:
    def histogram_color(self, frame1, frame2, thread_hold):
        hsv1 = cv.cvtColor(frame1, cv.COLOR_BGR2HSV)
        hist1 = cv.calcHist([hsv1], [0, 1], None, [180, 256], [0, 180, 0, 256])
        cv.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
        hsv2 = cv.cvtColor(frame2, cv.COLOR_BGR2HSV)
        hist2 = cv.calcHist([hsv2], [0, 1], None, [180, 256], [0, 180, 0, 256])
        cv.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
        dist = cv.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
        return dist