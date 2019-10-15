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
        frame_rate = 3

        #initialize motion detector class
        md = SingleMotionDetector(accumWeight=0.1)
        total = 0

        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            time_elapsed = time.time() - prev

            if time_elapsed > 1./frame_rate:
                #reset counter
                prev = time.time()

                #get frame and resize,convert to gray
                frame = imutils.resize(img, width=600)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # if the total number of frames has reached a sufficient
                # number to construct a reasonable background model, then
                # continue to process the frame
                if total > 10:
                    # detect motion in the image
                    motion = md.detect(gray)

                    # cehck to see if motion was found in the frame
                    if motion is not None:

                        
                        
                        
                        
                        
                        
                        #Save image of last movement:
                        cv2.imwrite(os.path.join(os.getcwd(),'last_movement.jpg'), frame)

                        # unpack the tuple and draw the box surrounding the
                        # "motion area" on the output frame
                        (thresh, (minX, minY, maxX, maxY)) = motion
                        cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                            (0, 0, 255), 2)

                        # encode as a jpeg image and return it
                        # grab the current timestamp and draw it on the frame
                        timestamp = datetime.datetime.now()
                        cv2.putText(frame, timestamp.strftime(
                        "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
                        
                        

                        #INSERT EMAIL HERE
                
                # update the background model and increment the total number
                # of frames read thus far
                md.update(gray)
                total += 1

                #yield cv2.imencode('.jpg', img)[1].tobytes()
            yield cv2.imencode('.jpg', frame)[1].tobytes()
