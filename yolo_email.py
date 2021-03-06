# This script is meant to be run constantly on the Raspberry Pi - it watches for
# changes in a motion capture image file and will run the Yolo V3 architecture
# on the image and email results using Gmail.
# By: Dustin Andrews
# Date: October 2019


from yolo_func import yolo_swag
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import pandas as pd
import time
import os
from os import path

# credentials file for GMAIL emailing
import credentials

# Get some config setup information
from config import config

# Set PATH
cwd = os.getcwd()

# Get object log to append class detections to. If it doesn't exist yet, create it. Not under version control.
if path.exists(os.path.join(cwd, "object_log.csv")):
    object_log = pd.read_csv(os.path.join(cwd, "object_log.csv"), index_col=False)
else:
    object_log = pd.DataFrame(columns=["class", "timestamp"])

# Setup infinite loop to check every 5 seconds for modified motion capture image
while True:
    check_time = time.time()

    # check if modified within last 5 seconds
    if (check_time - os.path.getmtime(os.path.join(cwd, "last_movement.jpg"))) < 5:

        email_switch = pd.read_csv(os.path.join(cwd, "email_switch.csv"))

        # check if emails are desired
        if email_switch["status"][0] == "email_on":

            # get yolo swaggin (run YoloNetV3 on image, get classLABELS back)
            classIDs = yolo_swag(
                os.path.join(cwd, "last_movement.jpg"),
                config["yolo_path"],
                0.5,
                0.3,
                os.path.join(cwd, "prediction.jpg"),
            )

            # Check if any objects detected are in config list
            if len(classIDs) > 0 and (
                any(i in config["email_object_classes"] for i in classIDs)
            ):

                timestamp = datetime.datetime.now()

                # Append to tracker log and save
                incr_df = pd.DataFrame(
                    [[x, timestamp] for x in classIDs], columns=("class", "timestamp")
                )
                object_log = pd.concat([object_log, incr_df])
                object_log.to_csv(os.path.join(cwd, "object_log.csv"), index=False)

                port = 465  # For SSL
                pwd = credentials.setup["GMAIL_PWD"]
                email = credentials.setup["GMAIL_EMAIL"]

                subject = (
                    "".join(x + "|" for x in classIDs)
                    + " detected "
                    + timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
                )
                body = "Motion captured in the house"
                sender_email = email
                receiver_email = credentials.setup["RECEIVER_EMAIL"]
                password = pwd

                # Create a multipart message and set headers
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject

                # Add body to email
                message.attach(MIMEText(body, "plain"))

                filename = os.path.join(
                    cwd, "prediction.jpg"
                )  # In same directory as script

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

                with smtplib.SMTP_SSL(
                    "smtp.gmail.com", port, context=context
                ) as server:
                    server.login(email, password)
                    server.sendmail(email, message["To"], text)
    else:
        time.sleep(1)