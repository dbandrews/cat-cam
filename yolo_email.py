from yolo_func import yolo_swag
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time
import os

#credentials file for GMAIL emailing
import credentials

#Set PATH
cwd = '/home/pi/cat-cam/'

#Setup infinite loop to check every 5 seconds for modified motion capture image

while True:
    check_time = time.time()

    #check if modified within last 5 seconds
    if (check_time - os.path.getmtime(os.path.join(cwd,'last_movement.jpg')))<5:
        
        #get yolo swaggin:
        classIDs = yolo_swag(os.path.join(cwd,'last_movement.jpg'),"/home/pi/darknet/cfg",0.5,0.3,os.path.join(cwd,'prediction.jpg'))

        #Check if any classes detected - just cat and person for now!
        if len(classIDs) > 0 and ('cat' in classIDs or 'person' in classIDs):

            port = 465  # For SSL
            pwd = credentials.setup['GMAIL_PWD']
            email = credentials.setup['GMAIL_EMAIL']

            timestamp = datetime.datetime.now()

            subject = "Motion Capture " + timestamp.strftime(
                        "%A %d %B %Y %I:%M:%S%p")
            body = "Motion captured in the house"
            sender_email = email
            receiver_email = "dustin.brown.andrews@gmail.com"
            password = pwd

            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject


            # Add body to email
            message.attach(MIMEText(body, "plain"))

            filename = os.path.join(cwd,'prediction.jpg')  # In same directory as script

            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()

            # Create a secure SSL context
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login(email, password)
                server.sendmail(email,message['To'],text)
    else:
        time.sleep(1)