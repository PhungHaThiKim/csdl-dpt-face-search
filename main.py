import cv2
import numpy as np
import cv2 as cv
import os
from algorithm.scenedetection.scenedetect import SceneDetection

fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
captured = False
total = 0
frames = 0
(W, H) = (700, 450)
cap = cv.VideoCapture('./data/001/001.mp4')

threshold = 15
last_mean = 0
while cap.isOpened():
    ret, frame = cap.read()
    # if frames is read correctly ret is True
    if not ret:
        print("Can't receive frames (stream end?). Exiting ...")
        break

    # frames = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
    orig = frame.copy()
    frame = cv2.resize(frame, (W, H))
    mask = fgbg.apply(frame)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    p = (cv2.countNonZero(mask) / float(W * H)) * 100

    if p < 20.0 and not captured and frames > 200:
        cv2.imshow("Captured", frame)
        captured = True
        filename = "{}.png".format(total)
        path = os.path.sep.join(["./data/001/frames", filename])
        total += 1
        print("[INFO] saving {}".format(path))
        cv2.imwrite(path, orig)
    elif captured and p >= 30.0:
        captured = False

    cv.imshow('frames', frame)
    cv2.imshow("Mask", mask)
    if cv.waitKey(1) == ord('q'):
        break

    frames += 1

cap.release()
cv.destroyAllWindows()