#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
from werkzeug.utils import secure_filename
import pandas as pd
import time


# Raspberry Pi camera module (requires picamera package)
#from camera_pi import Camera
from camera_opencv import Camera

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/email_switch_off')
def switch_email_off():
    pd.DataFrame({'status':['email_off']}).to_csv("email_switch.csv")
    return render_template('index.html')

@app.route('/email_switch_on')
def switch_email_on():
    pd.DataFrame({'status':['email_on']}).to_csv("email_switch.csv")
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, threaded=True)
