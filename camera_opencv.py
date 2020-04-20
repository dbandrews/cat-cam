import os
import cv2
from base_camera import BaseCamera
from motion_detection import SingleMotionDetector
import time
import datetime
import imutils


class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():

        prev = 0
        #restrict frame rate for serving externally over slower connections. 3 works for external serving over cell service.
        frame_rate = 50

        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            time_elapsed = time.time() - prev

            #Restrict frame rate for streaming over cellular?
            if time_elapsed > 1./frame_rate:
                #reset counter
                prev = time.time()

                #get frame and resize,convert to gray
                # frame = imutils.resize(img, width=800)
                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            
                #yield cv2.imencode('.jpg', img)[1].tobytes()
                yield cv2.imencode('.jpg', img)[1].tobytes()
