import pickle
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from shutil import copyfile, rmtree
import config
import os
import cv2 as cv
import numpy as np

from algorithm.facedetection.facedetect import FaceDetect
from algorithm.featureextraction.featureextract import FeatureExtract
from database import SessionLocal, engine
from algorithm.scenedetection.scenedetect import SceneDetection
import models

def insert_video(db: Session, path_src, datetime, des):
    video = models.Video(
        video_datetime=datetime,
        video_des=des
    )
    db.add(video)
    db.flush()

    video_folder = os.path.join(config.DATA_PATH, str(video.video_id).zfill(5))
    if not os.path.exists(video_folder):
        os.mkdir(video_folder)
    else:
        rmtree(video_folder)
        os.mkdir(video_folder)
    video_path = os.path.join(video_folder, "{}.mp4".format(str(video.video_id).zfill(5)))
    copyfile(path_src, video_path)
    video.video_folder = os.path.relpath(video_folder, config.DATA_PATH)
    video.video_path = os.path.relpath(video_path, config.DATA_PATH)
    db.flush()
    db.refresh(video)
    return video

def short_video(db: Session, video: models.Video):
    video_path = os.path.join(config.DATA_PATH, video.video_path)
    cap = cv.VideoCapture(video_path)
    fps = cap.get(cv.CAP_PROP_FPS)

    last_frame = None
    stackMean = None    # Stack mean(Frame)
    stackIndex = None   # Stack vi tri
    selectIndex = []
    short_start = []
    short_end = []
    fpss = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frames. Exiting ...")
            break
        # frame = cv2.resize(frame, (W, H))
        if last_frame is not None:
            # Nhan dien chuyen canh
            # Tinh do khac biet giua 2 frame dua vao khoang cach 2 histogram
            dist = SceneDetection().histogram_color(frame, last_frame)

            #Neu dat nguong khac biet giua 2 frame thi phat hien chuyen canh
            #Neu khong dat nguong thi tiep tuc stack cac frame va vi tri (coi nhu la dang trong shot)
            if dist > config.HISTOGRAM_DIST_THRESHOLD:
                if stackMean is not None:
                    print("StackShape", stackMean.shape)
                    meanstack = stackMean.mean() #Trung binh frame stack (pixel)
                    print("Mean", meanstack)
                    valMin = 1000000
                    valRet = -1

                    # Check trung binh Frame khong qua toi va time chuyen canh khong qua ngan (de ap dung cho chuyen canh mo dan va sang dan)
                    if meanstack > config.MEAN_FRAME_THRESHOLD and len(stackMean) > config.LEN_FRAME_THRESHOLD:
                        for i in range(len(stackMean)):
                            val = stackMean[i]
                            # So sanh lay frame gan voi frame trung binh nhat
                            if abs(val - meanstack) < valMin:
                                valMin = abs(val - meanstack)
                                valRet = stackIndex[i]

                        # Luu vi tri start_shot, end_shot, fps (cho front-end tach shot)
                        short_start.append(stackIndex[0])
                        short_end.append(stackIndex[-1])
                        fpss.append(fps)
                        #Lay vi tri frame dai dien cho shot do
                        selectIndex.append(valRet)
                    stackMean = None
                    stackIndex = None
            else:
                if stackMean is None:
                    stackMean = np.array([np.average(frame)])
                    stackIndex = np.array([cap.get(cv.CAP_PROP_POS_FRAMES)])
                else:
                    stackMean = np.append(stackMean, [np.average(frame)], axis=0)
                    stackIndex = np.append(stackIndex, [cap.get(cv.CAP_PROP_POS_FRAMES)], axis=0)
        last_frame = frame

    cap.release()

    # Tao folder vat ly
    frames_folder = os.path.join(config.DATA_PATH, video.video_folder, "frames")
    if not os.path.exists(frames_folder):
        os.mkdir(frames_folder)
    else:
        rmtree(frames_folder)
        os.mkdir(frames_folder)


    cap = cv.VideoCapture(video_path)

    frames = []
    # Lay frame dai dien dua vao vi tri da lay
    for id, sttFrame in enumerate(selectIndex):
        cap.set(cv.CAP_PROP_POS_FRAMES, sttFrame)
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frames. Exiting ...")
            break

        # Them vao db va folder vat ly
        framedb = models.Frame(
            frame_short_pos_start = short_start[id],
            frame_short_pos_end = short_end[id],
            frame_short_fps = fpss[id],
            video_id = video.video_id
        )
        db.add(framedb)
        db.flush()
        frame_name = "{}.png".format(str(framedb.frame_id).zfill(5))
        frame_path = os.path.join(frames_folder, frame_name)
        cv.imwrite(frame_path, frame)

        framedb.frame_path = os.path.relpath(frame_path, config.DATA_PATH)
        db.flush()
        db.refresh(framedb)

        frames.append(framedb)

    return frames


def face_detect(db: Session, frames: List[models.Frame]):
    faces_rs = []
    #Quet tung frame dai dien
    for frame in frames:
        faces_folder = os.path.join(config.DATA_PATH, frame.video.video_folder, "faces")

        frame_path = os.path.join(config.DATA_PATH, frame.frame_path)
        frameimg = cv.imread(frame_path)

        #detect cac face
        faces = FaceDetect.faces(frameimg)
        #cat cac face trong anh
        faces_crop = FaceDetect.faces_crop(frameimg, faces)

        if not os.path.exists(faces_folder):
            os.mkdir(faces_folder)

        # Voi moi face se duoc luu duong dan vao db va luu anh o folder vat ly
        for face in faces_crop:

            facedb = models.Face(
                frame_id=frame.frame_id
            )
            db.add(facedb)
            db.flush()

            face_name = "{}.png".format(str(facedb.face_id).zfill(5))
            face_path = os.path.join(faces_folder, face_name)
            cv.imwrite(face_path, face)
            print("Save:", face_path)

            facedb.face_path = os.path.relpath(face_path, config.DATA_PATH)
            db.flush()
            db.refresh(facedb)

            faces_rs.append(facedb)

    return faces_rs

def lbp_feature_extract(db: Session, faces: List[models.Face]):
    lbp_feature_rs = []

    # duyet tung face
    for face in faces:
        lbp_features_folder = os.path.join(config.DATA_PATH, face.frame.video.video_folder, "lbp_features")

        face_path = os.path.join(config.DATA_PATH, face.face_path)
        faceimg = cv.imread(face_path)

        #Extract feature local_binary_pattern
        feature = FeatureExtract.local_binary_pattern(faceimg)
        #Histogram muc xam feature
        feature_his = FeatureExtract.histogram_bit(feature)

        # Luu file_feature-path vao db va luu file_feature-data vao folder vat ly
        if not os.path.exists(lbp_features_folder):
            os.mkdir(lbp_features_folder)

        lbp_featuredb = models.LbpFeature(
            face_id=face.face_id
        )
        db.add(lbp_featuredb)
        db.flush()

        lbp_name = "{}.txt".format(str(lbp_featuredb.face_id).zfill(5))
        lbp_path = os.path.join(lbp_features_folder, lbp_name)
        with open(lbp_path, 'w') as file:
            np.savetxt(file, feature_his)
            # pickle.dump(feature, file)
        print("Save feature lbp:", lbp_path)

        lbp_featuredb.lbp_feature_path = os.path.relpath(lbp_path, config.DATA_PATH)
        db.flush()
        db.refresh(lbp_featuredb)

        lbp_feature_rs.append(lbp_featuredb)

    return lbp_feature_rs




if __name__ == "__main__":
    upload_folder = ".\\uploads"
    for f in os.listdir(upload_folder):
        file = os.path.join(upload_folder, f)

        srcpath_test = file
        db: Session = SessionLocal()
        video: models.Video = insert_video(db, srcpath_test, datetime=datetime.now(), des="1")
        frames: List[models.Frame] = short_video(db, video)
        faces: List[models.Face] = face_detect(db, frames)
        lbps: List[models.LbpFeature] = lbp_feature_extract(db, faces)
        print(video.__dict__)
        for f in frames:
            print(f.__dict__)
        for f in faces:
            print(f.__dict__)
        for l in lbps:
            print(l.__dict__)
        # db.rollback()
        db.commit()
        db.close()