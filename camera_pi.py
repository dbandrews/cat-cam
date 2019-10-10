import io
import time
import picamera
from base_camera import BaseCamera


class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)
            #set framerate, reducing for speed
            camera.framerate = 30

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',resize=(800,600),quality=5,
                                                 use_video_port=True):
               
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
