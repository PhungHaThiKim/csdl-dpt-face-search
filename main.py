import base64
import io
import math
from typing import List

from flask import Flask, render_template, send_from_directory, request, jsonify
from PIL import Image
import numpy as np

import models
import script_process_search
from database import SessionLocal
from sqlalchemy.orm import Session
import cv2 as cv

app = Flask(__name__, static_url_path='')

@app.route('/data/<path:path>')
def send_js(path):
    return send_from_directory('data', path)

def imageToBase64(imdt):
    imgprocess = Image.fromarray(imdt)
    rawBytes = io.BytesIO()
    imgprocess.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return img_base64

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/process", methods=["POST"])
def process_image():
    file = request.files['image']
    # print(file.stream)
    img = Image.open(file.stream)
    imagenp = np.array(img)
    imagenp = cv.cvtColor(imagenp, cv.COLOR_BGR2RGB)

    db: Session = SessionLocal()
    lbps, faces = script_process_search.search_image_euclidean(db, imagenp)

    faceTobase64 = imageToBase64(cv.cvtColor(faces[0], cv.COLOR_RGB2BGR))
    data = []
    for lbp in lbps:
        pos_start = lbp["lbp"].face.frame.frame_short_pos_start
        pos_end = lbp["lbp"].face.frame.frame_short_pos_end
        fps = lbp["lbp"].face.frame.frame_short_fps
        data.append({
            "video_path": lbp["lbp"].face.frame.video.video_path,
            "start_time": int(math.floor(pos_start/fps)),
            "end_time": int(math.ceil(pos_end/fps))
        })

    db.close()

    return jsonify({'result': True, 'data': data, 'message': str(faceTobase64)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)