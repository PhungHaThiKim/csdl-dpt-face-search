import cv2
import cv2 as cv
from skimage.feature import local_binary_pattern
import numpy as np

def get_pixel(img, center, x, y):
    new_value = 0
    try:
        if img[x][y] >= center:
            new_value = 1
    except:
        pass
    return new_value

def lbp_calculated_pixel(img, x, y):
    center = img[x][y]
    val_ar = []
    # top_left
    val_ar.append(get_pixel(img, center, x - 1, y - 1))
    # top
    val_ar.append(get_pixel(img, center, x - 1, y))
    # top_right
    val_ar.append(get_pixel(img, center, x - 1, y + 1))
    # right
    val_ar.append(get_pixel(img, center, x, y + 1))
    # bottom_right
    val_ar.append(get_pixel(img, center, x + 1, y + 1))
    # bottom
    val_ar.append(get_pixel(img, center, x + 1, y))
    # bottom_left
    val_ar.append(get_pixel(img, center, x + 1, y - 1))
    # left
    val_ar.append(get_pixel(img, center, x, y - 1))
    # Now, we need to convert binary
    # values to decimal
    power_val = [1, 2, 4, 8, 16, 32, 64, 128]
    val = 0
    for i in range(len(val_ar)):
        val += val_ar[i] * power_val[i]

    return val


class FeatureExtract:
    @staticmethod
    def histogram_color(img):
        hsv1 = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        hist1 = cv.calcHist([hsv1], [0, 1], None, [180, 256], [0, 180, 0, 256])
        cv.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
        return hist1

    @staticmethod
    def histogram_bit(img, rotation = False):
        if rotation:
            hist, _ = np.histogram(img, bins=np.arange(256+1), range=[0, 256], density=True)
        else:
            hist, _ = np.histogram(img, bins=256, range=[0, 256], density=True)
        return hist

    @staticmethod
    def local_binary_pattern(img):
        height, width, _ = img.shape
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        img_lbp = np.zeros((height, width),
                           np.uint8)
        for i in range(0, height):
            for j in range(0, width):
                img_lbp[i, j] = lbp_calculated_pixel(img, i, j)

        return img_lbp
