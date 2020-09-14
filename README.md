CAT-CAM: Motion Detection and Object Detection for Raspberry Pi 4
=====================

A Flask web streaming video app with motion detection. Motion capture images are run through Yolo V3 object detection and emailed using a configured Gmail account. Running the full Yolo v3 model takes ~7-10 seconds/image on the stock Raspberry Pi 4 with 4 GB RAM. If consecutive motion is detected this will introduce a lag in motion detection and emails of objects detected.

Object detection and emails can be switched on or off from the Flask app. Object detections are logged to a csv as well.

Setup:
- get OpenCv with python bindings pip installed (preferably into a virtualenv), gunicorn, nginx if wanting to run externally outside of local Wifi network
- Setup passwordless logins - no root login with passwords. SSH only with RSA key - remote development from Visual Studio Code or IDE of choice is recommended.
- Configure nginx for proper forwarding of requests to server 80 -> 443 (https)
- Can build in basic password protection using Nginx and SSL
- Download and install darknet (https://pjreddie.com/darknet/)
- Confirm paths for darknet to be run from yolo**** scripts
- Setup Supervisord tasks for both gunicorn server, and the Yolo_email script. Example supervisor configuration files included (example_supervisor_conf_*****). Be sure to change paths in these files to reflect your folder structure.
- Setup "credentials.py" in the same format given in example_credentials.py. Be sure to enable access for less secure apps to this email account (hopefully not your personal account): https://myaccount.google.com/lesssecureapps

TODO:
- [ ] Document/fix hardcoded paths/options

Based on code from excellent blogs: <br>
https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/ <br>
http://blog.miguelgrinberg.com/post/flask-video-streaming-revisited <br>

Links for Deploying Publicly Accesible Websites: <br>
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux <br>
https://www.digitalocean.com/community/tutorials/how-to-set-up-password-authentication-with-nginx-on-ubuntu-14-04 <br>




