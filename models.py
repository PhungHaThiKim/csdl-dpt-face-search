from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Video(Base):
    __tablename__ = 'video'

    video_id = Column(Integer, primary_key=True)
    video_folder = Column(String(255))
    video_path = Column(String(255))
    video_datetime = Column(DateTime, nullable=False)
    video_des = Column(String(255))


class Frame(Base):
    __tablename__ = 'frame'

    frame_id = Column(Integer, primary_key=True)
    frame_path = Column(String(255))
    frame_short_pos_start = Column(Integer, nullable=False)
    frame_short_pos_end = Column(Integer, nullable=False)
    frame_short_fps = Column(Integer, nullable=False)
    video_id = Column(ForeignKey('video.video_id'), nullable=False, index=True)

    video = relationship('Video')


class Face(Base):
    __tablename__ = 'face'

    face_id = Column(Integer, primary_key=True)
    face_path = Column(String(255))
    frame_id = Column(ForeignKey('frame.frame_id'), nullable=False, index=True)

    frame = relationship('Frame')


class SiftFeature(Base):
    __tablename__ = 'sift_feature'

    sift_feature_id = Column(Integer, primary_key=True)
    sift_feature_path = Column(String(255))
    face_id = Column(ForeignKey('face.face_id'), nullable=False, unique=True)

    face = relationship('Face')

class LbpFeature(Base):
    __tablename__ = 'lbp_feature'

    lbp_feature_id = Column(Integer, primary_key=True)
    lbp_feature_path = Column(String(255))
    face_id = Column(ForeignKey('face.face_id'), nullable=False, unique=True)

    face = relationship('Face')
