import cv2
import numpy as np
import cv2 as cv
import os
from algorithm.scenedetection.scenedetect import SceneDetection

cap = cv.VideoCapture('./data/001/001.mp4')
# (W, H) = (700, 450)

threshold = 15
last_mean = 0
last_frame = None
stackFrame = None
stackRet = None
selectRet = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frames (stream end?). Exiting ...")
        break
    # frame = cv2.resize(frame, (W, H))
    if last_frame is not None:
        dist = SceneDetection().histogram_color(frame, last_frame, 15)
        if dist > 70:
            if stackFrame is not None:
                # cv2.imshow("short", frames)
                print("StackShape", stackFrame.shape)
                meanstack = stackFrame.mean()
                print("Mean", meanstack)
                valMin = 1000000
                valRet = -1
                if meanstack > 10 and len(stackFrame) > 20:
                    for i in range(len(stackFrame)):
                        val = stackFrame[i]
                        if abs(val-meanstack) < valMin:
                            valMin = abs(val-meanstack)
                            valRet = stackRet[i]
                    selectRet.append(valRet)
                stackFrame = None
        else:
            if stackFrame is None:
                stackFrame = np.array([np.average(frame)])
                stackRet = np.array([cap.get(cv2.CAP_PROP_POS_FRAMES)])
            else:
                stackFrame = np.append(stackFrame, [np.average(frame)], axis=0)
                stackRet = np.append(stackRet, [cap.get(cv2.CAP_PROP_POS_FRAMES)], axis=0)

    last_frame = frame


    # cv.imshow('frames', frames)
    # if cv.waitKey(1) == ord('q'):
    #     break

cap.release()
cv.destroyAllWindows()

print(selectRet)

cap = cv.VideoCapture('./data/001/001.mp4')
stt = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frames (stream end?). Exiting ...")
        break
    # frame = cv2.resize(frame, (W, H))
    sttFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    if stt < len(selectRet) and sttFrame == selectRet[stt]:
        filename = "{}.png".format(stt)
        path = os.path.sep.join(["./data/001/frames", filename])
        cv.imshow('frames', frame)
        cv2.imwrite(path, frame)
        stt += 1
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()