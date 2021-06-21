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
    stackMean = None
    stackIndex = None
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

            dist = SceneDetection().histogram_color(frame, last_frame)
            if dist > config.HISTOGRAM_DIST_THRESHOLD:
                if stackMean is not None:
                    print("StackShape", stackMean.shape)
                    meanstack = stackMean.mean()
                    print("Mean", meanstack)
                    valMin = 1000000
                    valRet = -1
                    if meanstack > config.MEAN_FRAME_THRESHOLD and len(stackMean) > config.LEN_FRAME_THRESHOLD:
                        for i in range(len(stackMean)):
                            val = stackMean[i]
                            if abs(val - meanstack) < valMin:
                                valMin = abs(val - meanstack)
                                valRet = stackIndex[i]

                        short_start.append(stackIndex[0])
                        short_end.append(stackIndex[-1])
                        fpss.append(fps)
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
    cap = cv.VideoCapture(video_path)

    frames_folder = os.path.join(config.DATA_PATH, video.video_folder, "frames")
    if not os.path.exists(frames_folder):
        os.mkdir(frames_folder)
    else:
        rmtree(frames_folder)
        os.mkdir(frames_folder)

    frames = []

    for id, sttFrame in enumerate(selectIndex):
        cap.set(cv.CAP_PROP_POS_FRAMES, sttFrame)
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frames. Exiting ...")
            break

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
    for frame in frames:
        faces_folder = os.path.join(config.DATA_PATH, frame.video.video_folder, "faces")

        frame_path = os.path.join(config.DATA_PATH, frame.frame_path)
        frameimg = cv.imread(frame_path)

        faces = FaceDetect.faces(frameimg)

        faces_crop = FaceDetect.faces_crop(frameimg, faces)

        if not os.path.exists(faces_folder):
            os.mkdir(faces_folder)

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

def sift_feature_extract(db: Session, faces: List[models.Face]):
    sift_feature_rs = []
    for face in faces:
        sift_features_folder = os.path.join(config.DATA_PATH, face.frame.video.video_folder, "sift_features")

        face_path = os.path.join(config.DATA_PATH, face.face_path)
        faceimg = cv.imread(face_path)

        keyf, desf = FeatureExtract.sift(faceimg)

        if not os.path.exists(sift_features_folder):
            os.mkdir(sift_features_folder)

        sift_featuredb = models.SiftFeature(
            face_id=face.face_id
        )
        db.add(sift_featuredb)
        db.flush()

        sift_name = "{}.bin".format(str(sift_featuredb.face_id).zfill(5))
        sift_path = os.path.join(sift_features_folder, sift_name)
        with open(sift_path, 'wb') as file:
            pickle.dump((len(keyf), desf), file)
        print("Save feature sift:", sift_path)

        sift_featuredb.sift_feature_path = os.path.relpath(sift_path, config.DATA_PATH)
        db.flush()
        db.refresh(sift_featuredb)

        sift_feature_rs.append(sift_featuredb)

    return sift_feature_rs

def lbp_feature_extract(db: Session, faces: List[models.Face]):
    lbp_feature_rs = []
    for face in faces:
        lbp_features_folder = os.path.join(config.DATA_PATH, face.frame.video.video_folder, "lbp_features")

        face_path = os.path.join(config.DATA_PATH, face.face_path)
        faceimg = cv.imread(face_path)

        feature = FeatureExtract.local_binary_pattern(faceimg)

        if not os.path.exists(lbp_features_folder):
            os.mkdir(lbp_features_folder)

        lbp_featuredb = models.LbpFeature(
            face_id=face.face_id
        )
        db.add(lbp_featuredb)
        db.flush()

        lbp_name = "{}.bin".format(str(lbp_featuredb.face_id).zfill(5))
        lbp_path = os.path.join(lbp_features_folder, lbp_name)
        with open(lbp_path, 'wb') as file:
            pickle.dump(feature, file)
        print("Save feature lbp:", lbp_path)

        lbp_featuredb.lbp_feature_path = os.path.relpath(lbp_path, config.DATA_PATH)
        db.flush()
        db.refresh(lbp_featuredb)

        lbp_feature_rs.append(lbp_featuredb)

    return lbp_feature_rs




if __name__ == "__main__":
    upload_folder = "E:\\Banggioi\\Ky8\\CSDL DPT\\code\\csdl-dpt-face-search\\uploads"
    for f in os.listdir(upload_folder):
        file = os.path.join(upload_folder, f)

        srcpath_test = file
        db: Session = SessionLocal()
        video: models.Video = insert_video(db, srcpath_test, datetime=datetime.now(), des="1")
        frames: List[models.Frame] = short_video(db, video)
        faces: List[models.Face] = face_detect(db, frames)
        sifts: List[models.SiftFeature] = sift_feature_extract(db, faces)
        lbps: List[models.LbpFeature] = lbp_feature_extract(db, faces)
        print(video.__dict__)
        for f in frames:
            print(f.__dict__)
        for f in faces:
            print(f.__dict__)
        for s in sifts:
            print(s.__dict__)
        for l in lbps:
            print(l.__dict__)
        # db.rollback()
        db.commit()
        db.close()